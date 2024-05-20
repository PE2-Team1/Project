from src.get_lmz_path import *

# ------ Info & Options ------ #
info = {
    'script_description': "Process LMZ",
    'script_version': 0.1,
    'operator_name': "",
}
wafer = []  # ['D07', 'D08', ...]. Blank out list to process all wafers
device = ['LMZC', 'LMZO']
save_figure = True
export_csv = True
# ---------------------------- #

lmz_paths = get_lmz_path(wafer, device)

"""for lmz_path in lmz_paths:
    iv_process_result = {}
    trans_process_result = {}
    if save_figure:
        plot_figure(lmz_path, iv_process_result, trans_process_result)
    if export_csv:
        export_result(lmz_path, info, iv_process_result, trans_process_result)
"""