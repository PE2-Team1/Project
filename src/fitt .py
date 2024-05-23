import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
from get_lmz_path import *
import numpy as np
import pandas as pd
from lmfit import Parameters, Minimizer
from decimal import Decimal
from matplotlib.ticker import FuncFormatter
from scipy.signal import find_peaks

if __name__ == "__main__":
    lmz_paths = get_lmz_path()

    # Initialize an empty list to store the data dictionaries
    all_data = []

    for lmz_path in lmz_paths:
        tree = ET.parse(lmz_path)
        root = tree.getroot()

        voltage_str = root.find('.//Voltage').text
        voltage_values = np.array([float(v) for v in voltage_str.split(',')])
        current_str = root.find('.//Current').text
        current_values = np.array([float(v) for v in current_str.split(',')])
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


        pars = Parameters()
        pars.add('Is', value=10 ** -8)
        pars.add('Vt', value=0.026)
        pars.add('n', value=1, vary=False)

        fitter = Minimizer(mob, pars, fcn_args=(voltage_values, current_values))
        result = fitter.minimize()
        final = abs_current + result.residual

        RSS = np.sum(result.residual ** 2)
        mean_current = np.mean(current_values)
        TSS = np.sum((current_values - mean_current) ** 2)
        R_squared = 1 - (Decimal(RSS) / Decimal(TSS))

        fig, axs = plt.subplots(2, 2, figsize=(11, 7))


        def log_formatter(x, pos):
            return "{:.0e}".format(x)


        axs[0, 0].scatter(voltage_values, abs_current, label='data')
        axs[0, 0].plot(voltage_values, final, 'r-', label=f'fit ')
        axs[0, 0].set_xlim(-2, 1)
        axs[0, 0].set_yscale('log')
        axs[0, 0].yaxis.set_major_formatter(FuncFormatter(log_formatter))
        axs[0, 0].set_title('IV raw data & fitted data (log scale)')
        axs[0, 0].set_ylabel('Absolute Current (A)')
        axs[0, 0].set_xlabel('Voltage (V)')
        axs[0, 0].grid(True)
        axs[0, 0].legend(loc='upper left')

        values_to_display = [-2, -1, 1]
        for voltage, current in zip(voltage_values, abs_current):
            if voltage in values_to_display:
                current_text = f'{current:.6e}'
                voltage_str = f"{voltage:.1f}"
                axs[0, 0].annotate(current_text, (voltage, current), textcoords="offset points", xytext=(0, 5),
                                   ha='center')

        max_transmission_point = -50
        max_transmission_point2 = -50
        ref_transmission_point = -50
        max_transmission_wavelength = 1550
        max_transmission_wavelength2 = 1565

        for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):
            dc_bias = float(wavelengthsweep.get('DCBias'))
            if i == len(root.findall('.//WavelengthSweep')) - 1:
                label = None
            else:
                label = f'{dc_bias}V'
            wavelength_str = wavelengthsweep.find('.//L').text
            transmission_str = wavelengthsweep.find('.//IL').text

            wavelength_list = [float(w) for w in wavelength_str.split(',')]
            transmission_list = [float(t) for t in transmission_str.split(',')]

            axs[1, 0].plot(wavelength_list, transmission_list, label=label)

        axs[1, 0].set_xlabel('Wavelength (nm)')
        axs[1, 0].set_ylabel('Transmission (dB)')
        axs[1, 0].set_title('Transmission vs Wavelength')
        axs[1, 0].grid(True)
        axs[1, 0].legend(loc='lower right', bbox_to_anchor=(1.15, 0.5))

        reference_wave = wavelength_list
        reference_trans = transmission_list

        axs[0, 1].plot(reference_wave, reference_trans, label=f'data')

        degrees = range(1, 7)
        r_squared_values = {}

        for degree in degrees:
            coeffs, _, _, _ = np.linalg.lstsq(np.vander(reference_wave, degree + 1), reference_trans, rcond=None)
            polynomial = np.poly1d(coeffs)
            axs[0, 1].plot(reference_wave, polynomial(reference_wave), label=f'{degree}th')

            mean_transmission = np.mean(reference_trans)
            total_variation = np.sum((reference_trans - mean_transmission) ** 2)
            residuals = np.sum((transmission_list - polynomial(reference_wave)) ** 2)
            r_squared = 1 - (residuals / total_variation)
            r_squared_values[degree] = r_squared

            polynomials = []
            for i in range(degree, 0, -1):
                polynomials.append(f"{coeffs[degree - i]:.16f}X^{i}")
            polynomials.append(f"{coeffs[degree]:.16f}")
            polynomial_str = '+'.join(polynomials)

        max_transmission = np.max(reference_trans)
        min_transmission = np.min(reference_trans)
        x_pos = reference_wave[-1] - 0.5 * (reference_wave[-1] - reference_wave[0]) - 3.5
        y_pos = min_transmission + 0.9 * (max_transmission - min_transmission) - 4.4
        for degree, r_squared in r_squared_values.items():
            axs[0, 1].text(x_pos, y_pos, f'{degree}th R²: {r_squared:.4f}', fontsize=10, verticalalignment='top')
            y_pos -= 0.06 * (max_transmission - min_transmission)

        axs[0, 1].set_xlabel('Wavelength (nm)')
        axs[0, 1].set_ylabel('Transmission (dB)')
        axs[0, 1].set_title('Transmission spectra - Processed and fitting')
        axs[0, 1].grid(True)
        axs[0, 1].legend(loc='lower right')

        poly6 = polynomial(reference_wave)

        # Ensure both arrays have the same length
        min_length = min(len(transmission_list), len(poly6))
        transmission_list = transmission_list[:min_length]
        poly6 = poly6[:min_length]

        flat_transmission = np.array(transmission_list) - np.array(poly6)

        for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):
            if i != len(root.findall('.//WavelengthSweep')) - 1:
                peaks, _ = find_peaks(flat_transmission, distance=50)
                for peak_index in peaks:
                    if 1550 <= wavelength_list[peak_index] <= 1565:
                        if flat_transmission[peak_index] > max_transmission_point:
                            max_transmission_point = flat_transmission[peak_index]
                            max_transmission_wavelength = wavelength_list[peak_index]

            if i != len(root.findall('.//WavelengthSweep')) - 1:
                peaks, _ = find_peaks(flat_transmission, distance=50)
                for peak_index in peaks:
                    if 1565 <= wavelength_list[peak_index] <= 1580:
                        if flat_transmission[peak_index] > max_transmission_point2:
                            max_transmission_point2 = flat_transmission[peak_index]
                            max_transmission_wavelength2 = wavelength_list[peak_index]

        m = (max_transmission_point2 - max_transmission_point) / (
                max_transmission_wavelength2 - max_transmission_wavelength)
        b = max_transmission_point - m * max_transmission_wavelength
        peak_fit = m * np.array(wavelength_list) + b
        for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):
            dc_bias = float(wavelengthsweep.get('DCBias'))
            if i == len(root.findall('.//WavelengthSweep')) - 1:
                label = None
            else:
                label = f'{dc_bias}V'
            wavelength_str = wavelengthsweep.find('.//L').text
            transmission_str = wavelengthsweep.find('.//IL').text
            wavelength_list = [float(w) for w in wavelength_str.split(',')]
            transmission_list = [float(t) for t in transmission_str.split(',')]

            # Ensure all arrays have the same length
            min_length = min(len(transmission_list), len(poly6), len(peak_fit))
            wavelength_list = wavelength_list[:min_length]
            transmission_list = transmission_list[:min_length]
            poly6 = poly6[:min_length]
            peak_fit = peak_fit[:min_length]

            if i == len(root.findall('.//WavelengthSweep')) - 1:
                flat_transmission = np.array(transmission_list) - np.array(poly6)
            else:
                flat_transmission = np.array(transmission_list) - np.array(poly6) - np.array(peak_fit)
            axs[1, 1].plot(wavelength_list, flat_transmission, label=label)

        axs[1, 1].set_xlabel('Wavelength (nm)')
        axs[1, 1].set_ylabel('Flat Mearsured Transmission (dB)')
        axs[1, 1].set_title('Flat Transmission spectra -as measured')
        axs[1, 1].grid(True)
        axs[1, 1].legend(loc='lower right', bbox_to_anchor=(1.15, 0.5))
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.3)
        # 이미지를 저장할 디렉토리 설정
        save_directory = r"C:\Users\이현석\PycharmProjects\Project_LEE\res"

        # 이미지 저장
        plt.savefig(os.path.join(save_directory,
                                 f"{os.path.splitext(os.path.basename(lmz_path))[0]}_flat_transmission_spectra.png"))

        plt.close()

        data_dict = {key: [] for key in
                     ['Lot', 'Wafer', 'Mask', 'TestSite', 'Name', 'Date', 'Script ID', 'Script Version', 'Script Owner',
                      'Operator', 'Row', 'Column', 'ErrorFlag', 'Error description', 'Analysis Wavelength',
                      'Rsq of Ref. spectrum (Nth)', 'Max transmission of Ref. spec. (dB)', 'Rsq of IV', 'I at -1V [A]',
                      'I at 1V [A]']}

        test_site_info = root.find('.//TestSiteInfo')

        data_dict['Lot'].append(test_site_info.get('Batch'))
        data_dict['Wafer'].append(test_site_info.get('Wafer'))
        data_dict['Mask'].append(test_site_info.get('Maskset'))
        data_dict['TestSite'].append(test_site_info.get('TestSite'))
        data_dict['Operator'].append(root.get('Operator'))
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

        all_data.append(data_dict)

    csv_save_path = r"C:\Users\이현석\PycharmProjects\Project_LEE\res\Combined_AnalysisResult_A2.csv"
    # Combine all data dictionaries into a single DataFrame
    combined_df = pd.concat([pd.DataFrame(data) for data in all_data], ignore_index=True)

    # Write the combined DataFrame to a CSV file
    combined_df.to_csv(csv_save_path, index=False)

    pd.set_option('display.max_columns', None)
    print(combined_df.to_string(index=False))
