from src.get_lmz_path import *

# ------ Info & Options ------ #
script_description = "Process LMZ"
script_version = 0.1
operator_name = ""
wafer = ['D07']  # ['D07', 'D08', ...]. Blank out list to process all wafers
device = ['LMZC']
save_figure = True
export_csv = True
# ---------------------------- #

lmz_paths = get_lmz_path(wafer, device)

"""for lmz_path in lmz_paths:
    iv_process_result = {}
    trans_process_result = {}
    plot_figure(iv_process_result, trans_process_result, save_figure)
    if export_csv:
        export_result(iv_process_result, trans_process_result)
"""
