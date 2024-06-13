from src.get_lmz_path import get_lmz_path, analysis_time
from src.vi_process import vi
from src.plot_figure import plot_figure
from src.trans_process import *
from src.dataframe import make_new_data, append_data, export, data


def run(info, wafer, device, save_figure, export_csv):
    lmz_paths = get_lmz_path(wafer, device)
    i = 1
    for lmz_path in lmz_paths:
        device_name = lmz_path.split('\\')[4].split('.')[0]
        print(f"Processing {device_name} ({i}/{len(lmz_paths)})")
        vi_result = vi(lmz_path)
        trans_result = trans_process(lmz_path)
        if save_figure:
            plot_figure(vi_result, trans_result, lmz_path, analysis_time)
        if export_csv:
            result_dict = make_new_data(lmz_path, info, vi_result, trans_result)
            append_data(result_dict)

        i += 1
    if export_csv:
        export(data, analysis_time)


if __name__ == '__main__':
    _lmz_paths = get_lmz_path(['D07'], ['LMZC'])
    _vi_result = vi(_lmz_paths[0])
    _trans_result = trans_process(_lmz_paths[0])
    # plot_figure(_vi_result, 0, _lmz_paths[0])
    print(_trans_result)
