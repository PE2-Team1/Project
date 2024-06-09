import xml.etree.ElementTree as ET
import numpy as np
import warnings


def parse_trans(lmz_path):
    _transmission = {
        'vol': [],
        'l': [],
        'il': []
    }

    root = ET.parse(lmz_path).getroot()
    wavelength_sweep = root.findall('.//WavelengthSweep')

    for ws in wavelength_sweep[:-1]:
        _transmission['vol'].append(ws.attrib['DCBias'] + "V")
        _transmission['l'].append(np.array([float(_l) for _l in ws.find("L").text.split(",")]))
        _transmission['il'].append(np.array([float(_il) for _il in ws.find("IL").text.split(",")]))

    ref_ws = wavelength_sweep[-1]
    _ref = {
        'l': np.array([float(_l) for _l in ref_ws.find("L").text.split(",")]),
        'il': np.array([float(_il) for _il in ref_ws.find("IL").text.split(",")])
    }

    return _transmission, _ref


def to_ordinal(n) -> str:
    # cardinal to ordinal
    if n % 10 == 1 and n % 100 != 11:
        return str(n) + "st"
    elif n % 10 == 2 and n % 100 != 12:
        return str(n) + "nd"
    elif n % 10 == 3 and n % 100 != 13:
        return str(n) + "rd"
    else:
        return str(n) + "th"


def fit_ref(_ref):
    warnings.filterwarnings('ignore', message='Polyfit may be poorly conditioned')
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


def flatten(_transmission, _ref_models):
    peaks_l, peaks_il = [], []
    for b in range(len(_transmission['vol'])):
        bias_trans_l = _transmission['l'][b]
        bias_trans_il = _transmission['il'][b] - _ref_models[-1](_transmission['l'][b])
        max_il = np.max(bias_trans_il)
        max_l = bias_trans_l[np.where(bias_trans_il == max_il)[0][0]]
        peaks_l.append([max_l])
        peaks_il.append([max_il])
        if max_l > 1530:
            for i in range(2):
                peaks_il[b].append(peak_il := float(np.max(bias_trans_il[bias_trans_l > max_l + i * 10])))
                peaks_l[b].append(bias_trans_l[np.where(bias_trans_il == peak_il)[0][0]])
        else:
            for i in range(2):
                peaks_il[b].append(peak_il := float(np.max(bias_trans_il[bias_trans_l > max_l + i * 9])))
                peaks_l[b].append(bias_trans_l[np.where(bias_trans_il == peak_il)[0][0]])
    peak_models = [np.poly1d(np.polyfit(peaks_l[j], peaks_il[j], 1)) for j in range(len(peaks_l))]
    flat_trans = [
        _transmission['il'][k] - _ref_models[-1](_transmission['l'][k]) - peak_models[k](_transmission['l'][k]) for k in
        range(len(peaks_l))]
    return flat_trans


def trans_process(lmz_path):
    transmission, ref = parse_trans(lmz_path)
    ref_models, predicted_il_list, fit_label_list, ref_r2_score_list = fit_ref(ref)
    flat_trans = flatten(transmission, ref_models)
    result = {
        'DCBias': transmission['vol'],
        'transmission_l': transmission['l'],
        'transmission_il': transmission['il'],
        'ref_l': ref['l'],
        'ref_il': ref['il'],
        'ref_max': np.max(ref['il']),
        'ref_model_list': ref_models,
        'ref_pred_il': predicted_il_list,
        'ref_fit_label': fit_label_list,
        'ref_r2_score_list': ref_r2_score_list,
        'flat_transmission': flat_trans
    }
    return result


if __name__ == '__main__':
    path = '../dat/HY202103/D07/20190715_190855/HY202103_D07_(0,0)_LION1_DCM_LMZC.xml'
    __, __ref = parse_trans(path)
    print(fit_ref(__ref))