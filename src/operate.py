from src.get_lmz_path import get_lmz_path
from src.vi_process import vi
from src.plot_figure import plot_figure


def run(info, wafer, device, save_figure, export_csv):
    lmz_paths = get_lmz_path(wafer, device)
    for lmz_path in lmz_paths:
        vi_result = vi(lmz_path)
        trans_result = 0
        plot_figure(vi_result, trans_result, lmz_path)


if __name__ == '__main__':
    lmz_paths = get_lmz_path(['D07'], ['LMZC'])
    vi_result = vi(lmz_paths[0])
    plot_figure(vi_result, 0, lmz_paths[0])
