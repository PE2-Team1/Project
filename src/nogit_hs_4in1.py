import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lmfit import Parameters, Minimizer
from decimal import Decimal
from matplotlib.ticker import FuncFormatter
from scipy.signal import find_peaks


# Parse the XML file and get the root element
tree = elemTree.parse("HY202103_D07_(0,0)_LION1_DCM_LMZC.xml")
root = tree.getroot()

print ('\n--- IV raw data & fitted --- \n')
# Parsing using find method
voltage_str = root.find('.//Voltage').text
# Change str to list
voltage_values = np.array([float(v) for v in voltage_str.split(',')])
print("Voltage:", ', '.join(map(str, voltage_values)))
current_str = root.find('.//Current').text
current_values = np.array([float(v) for v in current_str.split(',')])
print("Current:", ', '.join(map(str, current_values)))
# Absolute value for current value
abs_current = np.abs(current_values)

def mob(params, x, data=None):
    Is = params['Is']
    Vt = params['Vt']
    n = params['n']
    poly_coeff = np.polyfit(x[x < 0], data[x < 0], deg=2)
    model_negative = np.polyval(poly_coeff, x[x < 0])
    model_positive = Is * (np.exp(x[x >= 0] / (n * Vt)) - 1)
    model = np.concatenate((model_negative, model_positive))
    if data is None:
        return model
    else:
        return model - data

# Set up the initial parameter values
pars = Parameters()
pars.add('Is', value=10**-8)
pars.add('Vt', value=0.026)
pars.add('n', value=1, vary=False)

fitter = Minimizer(mob, pars, fcn_args=(voltage_values, current_values))
result = fitter.minimize()
final = abs_current + result.residual
print("fit:", ', '.join(map(str, final)))

# Calculate R-squared
RSS = np.sum(result.residual ** 2)
mean_current = np.mean(current_values)
TSS = np.sum((current_values - mean_current) ** 2)
R_squared = 1 - (Decimal(RSS) / Decimal(TSS))
print("R²:", R_squared)

# Initialize figure and axes for subplots
fig, axs = plt.subplots(2, 2, figsize=(11, 7))
def log_formatter(x, pos):
    return "{:.0e}".format(x)
# First subplot: IV raw data & fitted data
axs[0, 0].scatter(voltage_values, abs_current, label='data')
axs[0, 0].plot(voltage_values, final, 'r-', label=f'fit (R²: {R_squared:.4f})')
axs[0, 0].set_xlim(-2, 1)
axs[0, 0].set_yscale('log')
axs[0, 0].yaxis.set_major_formatter(FuncFormatter(log_formatter))
axs[0, 0].set_title('IV raw data & fitted data (log scale)')
axs[0, 0].set_ylabel('Voltage (V)')
axs[0, 0].set_xlabel('Absolute Current (A)')
axs[0, 0].grid(True)
axs[0, 0].legend(loc='upper left')

# Display current values at -2V, -1V, 1V
values_to_display = [-2, -1, 1]
for voltage, current in zip(voltage_values, abs_current):
    if voltage in values_to_display:
        current_text = f'{current:.6e}'
        voltage_str = f"{voltage:.1f}"
        axs[0, 0].annotate(current_text, (voltage, current), textcoords="offset points", xytext=(0, 5), ha='center')
        print(f"Current value at {voltage_str:>5}V: {current_text}")

print ('\n--- Transmission vs Wavelength --- \n')
# Initialize variables to store the maximum transmission points and their corresponding wavelengths
max_transmission_point = -50
max_transmission_point2 = -50
ref_transmission_point = -50
max_transmission_wavelength = 1550
max_transmission_wavelength2 = 1565

# Second subplot: Transmission vs Wavelength
for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):
    dc_bias = float(wavelengthsweep.get('DCBias'))
    # Do not display legend for the last DCBias
    if i == len(root.findall('.//WavelengthSweep')) - 1:
        label = None
    else:
        label = f'{dc_bias}V'
    # Extract wavelength and transmission data
    wavelength_str = wavelengthsweep.find('.//L').text
    transmission_str = wavelengthsweep.find('.//IL').text

    # Convert strings to lists
    wavelength_list = [float(w) for w in wavelength_str.split(',')]
    transmission_list = [float(t) for t in transmission_str.split(',')]

    # Exclude the last graph

    # Plot the graph
    axs[1, 0].plot(wavelength_list, transmission_list, label=label)

# Set labels and title for the second subplot
axs[1, 0].set_xlabel('Wavelength (nm)')
axs[1, 0].set_ylabel('Transmission (dB)')
axs[1, 0].set_title('Transmission vs Wavelength')
axs[1, 0].grid(True)
axs[1, 0].legend(loc='lower right', bbox_to_anchor=(1.15, 0.5))

print('\n--- Transmission spectra - Processed and fitting ---\n')
# Plot
reference_wave = wavelength_list
reference_trans = transmission_list

axs[0, 1].plot(reference_wave, reference_trans, label=f'data')

# Polynomial degree
degrees = range(1, 7)

# Store R-squared values
r_squared_values = {}

# Fit polynomials and plot
for degree in degrees:
    # Fit polynomial with no rank warning
    coeffs, _, _, _ = np.linalg.lstsq(np.vander(reference_wave, degree + 1), reference_trans, rcond=None)

    # Create polynomial from coefficients
    polynomial = np.poly1d(coeffs)

    # Plot polynomial
    axs[0, 1].plot(reference_wave, polynomial(reference_wave), label=f'{degree}th')

    # Calculate R-squared
    mean_transmission = np.mean(reference_trans)
    total_variation = np.sum((reference_trans - mean_transmission) ** 2)
    residuals = np.sum((transmission_list - polynomial(reference_wave)) ** 2)
    r_squared = 1 - (residuals / total_variation)

    # Store R-squared values
    r_squared_values[degree] = r_squared

    # Print polynomial and R-squared value
    polynomials = []
    for i in range(degree, 0, -1):
        polynomials.append(f"{coeffs[degree - i]:.16f}X^{i}")
    polynomials.append(f"{coeffs[degree]:.16f}")
    polynomial_str = '+'.join(polynomials)
    print(f'{degree}th polynomial:', polynomial_str)
    print(f'{degree}th R²:', r_squared)

# Position for R-squared values
max_transmission = np.max(reference_trans)
min_transmission = np.min(reference_trans)
x_pos = reference_wave[-1] - 0.5 * (reference_wave[-1] - reference_wave[0]) - 3.5
y_pos = min_transmission + 0.9 * (max_transmission - min_transmission) - 4.4
for degree, r_squared in r_squared_values.items():
    axs[0, 1].text(x_pos, y_pos, f'{degree}th R²: {r_squared:.4f}', fontsize=10, verticalalignment='top')
    y_pos -= 0.06 * (max_transmission - min_transmission)

# Plot settings
axs[0, 1].set_xlabel('Wavelength (nm)')
axs[0, 1].set_ylabel('Transmission (dB)')
axs[0, 1].set_title('Transmission spectra - Processed and fitting')
axs[0, 1].grid(True)
axs[0, 1].legend(loc='lower right')

print ('\n--- Flat Transmission spectra -as measured ---\n')
poly6 = polynomial(reference_wave)
for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):

    # Extract wavelength and transmission data
    wavelength_str = wavelengthsweep.find('.//L').text
    transmission_str = wavelengthsweep.find('.//IL').text

    # Convert strings to lists
    wavelength_list = [float(w) for w in wavelength_str.split(',')]
    transmission_list = [float(t) for t in transmission_str.split(',')]

    flat_transmission = np.array(transmission_list) - np.array(poly6)

    if i != len(root.findall('.//WavelengthSweep')) - 1:
        # Find peaks in transmission data
        peaks, _ = find_peaks(flat_transmission, distance=50)  # Adjust distance parameter as needed

        # Iterate through peaks and find the one within the specified wavelength range
        for peak_index in peaks:
            if 1550 <= wavelength_list[peak_index] <= 1565:
                # Update maximum transmission point if the peak is higher
                if flat_transmission[peak_index] > max_transmission_point:
                    max_transmission_point = flat_transmission[peak_index]
                    max_transmission_wavelength = wavelength_list[peak_index]

    if i != len(root.findall('.//WavelengthSweep')) - 1:
        # Find peaks in transmission data
        peaks, _ = find_peaks(flat_transmission, distance=50)  # Adjust distance parameter as needed

        # Iterate through peaks and find the one within the specified wavelength range
        for peak_index in peaks:
            if 1565 <= wavelength_list[peak_index] <= 1580:
                # Update maximum transmission point if the peak is higher
                if flat_transmission[peak_index] > max_transmission_point2:
                    max_transmission_point2 = flat_transmission[peak_index]
                    max_transmission_wavelength2 = wavelength_list[peak_index]

# Print the maximum transmission points and their corresponding wavelengths
print("First Peak Wavelength:", max_transmission_wavelength, "nm")
print("First Peak Transmission:", max_transmission_point, "dB")
print("Second Peak Wavelength:", max_transmission_wavelength2, "nm")
print("Second Peak Transmission:", max_transmission_point2, "dB")
m = (max_transmission_point2 - max_transmission_point) / (
                max_transmission_wavelength2 - max_transmission_wavelength)
b = max_transmission_point - m * max_transmission_wavelength
print(f"Equation of the line: y = {m}x + {b}")
peak_fit = m * np.array(wavelength_list) + b
for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):
    dc_bias = float(wavelengthsweep.get('DCBias'))
    # Do not display legend for the last DCBias
    if i == len(root.findall('.//WavelengthSweep')) - 1:
        label = None
    else:
        label = f'{dc_bias}V'
    # Extract wavelength and transmission data
    wavelength_str = wavelengthsweep.find('.//L').text
    transmission_str = wavelengthsweep.find('.//IL').text

    # Convert strings to lists
    wavelength_list = [float(w) for w in wavelength_str.split(',')]
    transmission_list = [float(t) for t in transmission_str.split(',')]
    if i == len(root.findall('.//WavelengthSweep')) - 1:
        flat_transmission = np.array(transmission_list) - np.array(poly6)
    else:
        flat_transmission = np.array(transmission_list) - np.array(poly6) - np.array(peak_fit )
    axs[1, 1].plot(wavelength_list, flat_transmission, label=label)

# Set labels and title for the second subplot

axs[1, 1].set_xlabel('Wavelength (nm)')
axs[1, 1].set_ylabel('Flat Mearsured Transmission (dB)')
axs[1, 1].set_title('Flat Transmission spectra -as measured')
axs[1, 1].grid(True)
axs[1, 1].legend(loc='lower right', bbox_to_anchor=(1.15, 0.5))

print ('\n--- Analysis Result A2 ---\n')
# Initialize the dictionary to store necessary information
data_dict = {key: [] for key in ['Lot', 'Wafer', 'Mask', 'TestSite', 'Name', 'Date', 'Script ID', 'Script Version', 'Script Owner', 'Operator', 'Row', 'Column','ErrorFlag', 'Error description', 'Analysis Wavelength', 'Rsq of Ref. spectrum (Nth)', 'Max transmission of Ref. spec. (dB)', 'Rsq of IV', 'I at -1V [A]','I at 1V [A]']}

# Extract Row and Column information from XML
test_site_info = root.find('.//TestSiteInfo')

# Extract Lot, Wafer, Mask, TestSite information from XML
data_dict['Lot'].append(test_site_info.get('Batch'))
data_dict['Wafer'].append(test_site_info.get('Wafer'))
data_dict['Mask'].append(test_site_info.get('Maskset'))
data_dict['TestSite'].append(test_site_info.get('TestSite'))

# Extract Operator information from XML
data_dict['Operator'].append(root.get('Operator'))

# Extract ModulatorSite information from ElectroOpticalMeasurements
modulator_site = root.find('.//ElectroOpticalMeasurements/ModulatorSite')
if modulator_site is not None:
    modulator = modulator_site.find('.//Modulator')
    data_dict['Name'].append(modulator.get('Name'))
data_dict['Script ID'].append(modulator.get('ScriptID', 'Process LMZ'))
data_dict['Script Version'].append(modulator.get('ScriptVersion', '0.1'))
data_dict['Script Owner'].append(modulator.get('ScriptOwner', 'A2'))

date_stamp = root.find('.//PortCombo').get('DateStamp')
data_dict['Date'].append(date_stamp)

data_dict['Row'].append(test_site_info.get('DieRow'))
data_dict['Column'].append(test_site_info.get('DieColumn'))

if float(r_squared) < 0.95:
    data_dict['ErrorFlag'].append('1')
    data_dict['Error description'].append('Ref. spec. Error')
else:
    data_dict['ErrorFlag'].append('0')
    data_dict['Error description'].append('No Error')

data_dict['Analysis Wavelength'].append('1550')

data_dict['Rsq of Ref. spectrum (Nth)'].append(r_squared)
data_dict['Max transmission of Ref. spec. (dB)'].append(ref_transmission_point)
data_dict['Rsq of IV'].append(R_squared)

values_to_display = [-1, 1]
for voltage, current in zip(voltage_values, abs_current):
    if voltage == -1:
        data_dict['I at -1V [A]'].append(current)
    elif voltage == 1:
        data_dict['I at 1V [A]'].append(current)

# Convert extracted information into a DataFrame
df = pd.DataFrame(data_dict)

# Print the result
pd.set_option('display.max_columns', None)
print(df.to_string(index=False))
df.to_csv('AnalysisResult_A2.csv', index=False)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.subplots_adjust(hspace=0.3)
plt.show()