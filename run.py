from src.operate import run

# ------ Info & Options ------ #
info = {
    'script_id': "Process LMZ",
    'script_owner': 'Team 1',
    'script_version': '1.0.0',
    'operator_name': "",
}
wafer = []  # ['D07', 'D08', ...]. Blank out list to process all wafers
device = ['LMZC', 'LMZO']
save_figure = True
export_excel = True
# ---------------------------- #

run(info, wafer, device, save_figure, export_excel)
