from get_lmz_path import get_lmz_path


def run(info, wafer, device, save_figure, export_csv):
    lmz_paths = get_lmz_path(wafer, device)
    """for lmz_path in lmz_paths:
        iv_result = iv_process(lmz_path)
    """


if __name__ == '__main__':
    run(0, ['D07'], ['LMZC'], 0, 0)
