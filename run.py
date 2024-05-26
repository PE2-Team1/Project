import src.operate as operate

# ------ Info & Options ------ #
info = {
    'script_id': "Process LMZ",
    'script_owner': 'Group 1',
    'script_version': 0.1,
    'operator_name': "",
}
wafer = ['D07']  # ['D07', 'D08', ...]. Blank out list to process all wafers
device = ['LMZC']
save_figure = True
export_csv = True
# ---------------------------- #

operate.run(info, wafer, device, save_figure, export_csv)
