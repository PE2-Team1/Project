import xml.etree.ElementTree as elemTree
import numpy as np
from scipy.signal import find_peaks

def trans_process(lmz_path):
    # Parse the XML file and get the root element
    tree = elemTree.parse(lmz_path)
    root = tree.getroot()

    # Initialize variables to store the maximum transmission points and their corresponding wavelengths
    max_transmission_point = -50
    max_transmission_point2 = -50
    max_transmission_wavelength = 1550
    max_transmission_wavelength2 = 1565

    for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):
        wavelength_str = wavelengthsweep.find('.//L').text
        transmission_str = wavelengthsweep.find('.//IL').text
        wavelength_list = [float(w) for w in wavelength_str.split(',')]
        transmission_list = [float(t) for t in transmission_str.split(',')]

    # Find all WavelengthSweep elements
    wavelength_sweeps = root.findall('.//WavelengthSweep')

    # Get the last WavelengthSweep element
    last_wavelength_sweep = wavelength_sweeps[-1]

    # Extract L and IL data from the last WavelengthSweep element
    ref_L = np.array([float(l) for l in last_wavelength_sweep.find("L").text.split(",")])
    ref_IL = np.array([float(il) for il in last_wavelength_sweep.find("IL").text.split(",")])

    # Assign reference_wave and reference_trans to the last WavelengthSweep data
    reference_wave = ref_L
    reference_trans = ref_IL

    # Find the maximum transmission value from the reference transmission data
    ref_max = np.max(reference_trans)

# ref fit

    # Polynomial degree
    degrees = range(1, 7)

    # Store R-squared values
    r_squared_values = {}

    for degree in degrees:
        # Fit polynomial with no rank warning
        coeffs, _, _, _ = np.linalg.lstsq(np.vander(reference_wave, degree + 1), reference_trans, rcond=None)

        # Create polynomial from coefficients
        polynomial = np.poly1d(coeffs)

        # Calculate R-squared
        mean_transmission = np.mean(reference_trans)
        total_variation = np.sum((reference_trans - mean_transmission) ** 2)
        residuals = np.sum((transmission_list - polynomial(reference_wave)) ** 2)
        r_squared = 1 - (residuals / total_variation)

        # Store R-squared values
        r_squared_values[degree] = r_squared

    # flat fit

    # Fit polynomial to the reference transmission data
    poly6 = polynomial(reference_wave)
    for i, wavelengthsweep in enumerate(root.findall('.//WavelengthSweep')):
        flat_transmission = np.array(transmission_list) - np.array(poly6)

        if i != len(root.findall('.//WavelengthSweep')) - 1:
            # Find peaks in transmission data
            peaks, _ = find_peaks(flat_transmission, distance=50)  # Adjust distance parameter as needed

            # Iterate through peaks and find the one within the specified wavelength range
            for peak_index in peaks:
                if 1310 <= wavelength_list[peak_index] <= 1325:
                    # Update maximum transmission point if the peak is higher
                    if flat_transmission[peak_index] > max_transmission_point2:
                        max_transmission_point2 = flat_transmission[peak_index]
                        max_transmission_wavelength2 = wavelength_list[peak_index]

        if i != len(root.findall('.//WavelengthSweep')) - 1: # 마지막 아닐 때
            # Find peaks in transmission data
            peaks, _ = find_peaks(flat_transmission, distance=50)  # Adjust distance parameter as needed

            # Iterate through peaks and find the one within the specified wavelength range
            for peak_index in peaks:
                if 1325 <= wavelength_list[peak_index] <= 1340:
                    # Update maximum transmission point if the peak is higher
                    if flat_transmission[peak_index] > max_transmission_point:
                        max_transmission_point = flat_transmission[peak_index]
                        max_transmission_wavelength = wavelength_list[peak_index]

        if i != len(root.findall('.//WavelengthSweep')) - 1: # 마지막 아닐 때
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
    m = (max_transmission_point2 - max_transmission_point) / (
            max_transmission_wavelength2 - max_transmission_wavelength)
    b = max_transmission_point - m * max_transmission_wavelength  # "Equation of the line: y = {m}x + {b}"

    # peak_fit
    peak_fit = m * np.array(wavelength_list) + b

    # Return the required values
    return { 'wavelength' : wavelength_list,
             'transmission' : transmission_list,
             'reference_wave' : reference_wave,
             'reference_trans' : reference_trans,
             'reference_max' : ref_max,
             'ref_fit' : polynomial,
             'flat_fit' : poly6,
             'peak_fit' : peak_fit,
             'r_squared' : r_squared}
    # r_squared을 호출할 때 1차 : r_squared[0], 2차 : r_squared[1] . . .

