import xml.etree.ElementTree as ET
import numpy as np
from scipy.signal import find_peaks


# Parsing function to extract data from XML
def parse_trans(lmz_path):
    _transmission = {
        'vol': [],
        'l': [],
        'il': []
    }

    root = ET.parse(lmz_path).getroot()
    wavelength_sweep = root.findall('.//WavelengthSweep')

    for ws in wavelength_sweep[:-1]:  # Exclude the last element
        _transmission['vol'].append(ws.attrib['DCBias'] + "V")
        _transmission['l'].append(np.array([float(_l) for _l in ws.find("L").text.split(",")]))
        _transmission['il'].append(np.array([float(_il) for _il in ws.find("IL").text.split(",")]))

    ref_ws = wavelength_sweep[-1]
    _ref = {
        'l': np.array([float(_l) for _l in ref_ws.find("L").text.split(",")]),
        'il': np.array([float(_il) for _il in ref_ws.find("IL").text.split(",")])
    }

    return _transmission, _ref


# Function to convert cardinal to ordinal
def to_ordinal(n) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return str(n) + "st"
    elif n % 10 == 2 and n % 100 != 12:
        return str(n) + "nd"
    elif n % 10 == 3 and n % 100 != 13:
        return str(n) + "rd"
    else:
        return str(n) + "th"


# Function to fit reference data to polynomial models
def fit_ref(_ref):
    fit_degrees = range(1, 7)
    ref_models = [np.poly1d(np.polyfit(_ref['l'], _ref['il'], deg)) for deg in fit_degrees]
    predicted_il_list = np.array([ref_models[i](_ref['l']) for i in range(len(ref_models))])
    fit_label_list = [to_ordinal(i) for i in fit_degrees]

    ref_r2_score_list = []
    for i in range(len(ref_models)):
        sst = np.sum((_ref['il'] - np.mean(_ref['il'])) ** 2)
        ssr = np.sum((_ref['il'] - predicted_il_list[i]) ** 2)
        ref_r2_score_list.append(1 - ssr / sst)

    return ref_models, predicted_il_list, fit_label_list, ref_r2_score_list


# Function to flatten the transmission data using the reference data and flat fit
def flatten(_transmission, _ref):
    poly6 = fit_ref(_ref)[0][5]  # Using the 6th degree polynomial fit for reference
    for i, (_transmission['l'], _transmission['il']) in enumerate(zip(_transmission['l'], _transmission['il'])):
        flat_transmission = np.array(_transmission['il']) - np.array(poly6(wavelength_list))

        if i != len(_transmission['l']) - 1:
            # Find peaks in transmission data
            peaks, _ = find_peaks(flat_transmission, distance=50)

            # Iterate through peaks and find the one within the specified wavelength range
            for peak_index in peaks:
                if 1310 <= wavelength_list[peak_index] <= 1325:
                    if flat_transmission[peak_index] > max_transmission_point2:
                        max_transmission_point2 = flat_transmission[peak_index]
                        max_transmission_wavelength2 = wavelength_list[peak_index]

            for peak_index in peaks:
                if 1325 <= wavelength_list[peak_index] <= 1340:
                    if flat_transmission[peak_index] > max_transmission_point:
                        max_transmission_point = flat_transmission[peak_index]
                        max_transmission_wavelength = wavelength_list[peak_index]

            for peak_index in peaks:
                if 1550 <= wavelength_list[peak_index] <= 1565:
                    if flat_transmission[peak_index] > max_transmission_point:
                        max_transmission_point = flat_transmission[peak_index]
                        max_transmission_wavelength = wavelength_list[peak_index]

            for peak_index in peaks:
                if 1565 <= wavelength_list[peak_index] <= 1580:
                    if flat_transmission[peak_index] > max_transmission_point2:
                        max_transmission_point2 = flat_transmission[peak_index]
                        max_transmission_wavelength2 = wavelength_list[peak_index]

    # Calculate slope (m) and intercept (b) for flat fit
    m = (max_transmission_point2 - max_transmission_point) / (
                max_transmission_wavelength2 - max_transmission_wavelength)
    b = max_transmission_point - m * max_transmission_wavelength

    # Compute flat fit
    peak_fit = m * np.array(wavelength_list) + b

    return flat_transmission, peak_fit


# Example usage
transmission, ref = parse_trans('HY202103_D07_(0,0)_LION1_DCM_LMZC.xml')
flat_transmission, peak_fit = flatten(transmission, ref)
print(flat_transmission)
print(peak_fit)
