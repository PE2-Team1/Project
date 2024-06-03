import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
import xml.etree.ElementTree as ET
from datetime import datetime

data = {
    'Batch': [],
    'Wafer': [],
    'Mask': [],
    'TestSite': [],
    'Name': [],
    'Date': [],
    'Script ID': [],
    'Script Version': [],
    'Script Owner': [],
    'Operator': [],
    'Row': [],
    'Column': [],
    'Error Flag': [],
    'Error Desc.': [],
    'Analysis Wavelength (nm)': [],
    'Rsq of Ref. spectrum (6th)': [],
    'Max transmission of Ref. spectrum (dBm)': [],
    'Rsq of IV': [],
    'I at -1V (A)': [],
    'I at +1V (A)': [],
    'Plot Image': [],
    'XML Path': []
}


def append_data(new_dict):
    global data
    for key in new_dict.keys():
        data[key].append(new_dict[key])


def make_new_data(lmz_path, info, iv, trans):
    root = ET.parse(lmz_path).getroot()
    test_site_info = root.find('.//TestSiteInfo').attrib
    date = root.find('.//PortCombo').attrib['DateStamp']
    formatted_date = datetime.strptime(date, "%a %b %d %H:%M:%S %Y").strftime("%Y%m%d_%H%M%S")
    des_wavelength = root.findall('.//DesignParameter')[1].text
    new_data = {
        'Batch': test_site_info['Batch'],
        'Wafer': test_site_info['Wafer'],
        'Mask': test_site_info['Maskset'],
        'TestSite': test_site_info['TestSite'],
        'Name': root.find('.//Modulator').attrib['Name'],
        'Date': formatted_date,
        'Script ID': info['script_id'],
        'Script Version': info['script_version'],
        'Script Owner': info['script_owner'],
        'Operator': info['operator_name'],
        'Row': int(test_site_info['DieRow']),
        'Column': int(test_site_info['DieColumn']),
        'Error Flag': "",
        'Error Desc.': "",
        'Analysis Wavelength (nm)': int(des_wavelength),
        'Rsq of Ref. spectrum (6th)': trans['ref_r2_score_list'][-1],
        'Max transmission of Ref. spectrum (dBm)': trans['ref_max'],
        'Rsq of IV': iv['R_squared'],
        'I at -1V (A)': iv['abs_current'][4],
        'I at +1V (A)': iv['abs_current'][12],
        'Plot Image': '',
        'XML Path': lmz_path
    }
    if new_data['Rsq of Ref. spectrum (6th)'] < 0.998:
        new_data['Error Flag'] = 1
        new_data['Error Desc.'] = 'Low Rsq of Ref.'
    return new_data


def export(_data):
    df = pd.DataFrame(_data)
    df2 = df.drop(columns=['XML Path'], inplace=False)
    # Create new workbook
    wb = Workbook()
    ws = wb.active

    # Write data into Excel sheet
    for r in dataframe_to_rows(df2, index=False, header=True):
        ws.append(r)

    # Adding hyperlinks
    i = 2
    while i <= len(_data['Batch']) + 1:
        row_xl = i
        col_xl = 21
        batch = _data['Batch'][i - 2]
        wafer = _data['Wafer'][i - 2]
        date = _data['XML Path'][i - 2].split('\\')[3]
        row = _data['Row'][i - 2]
        col = _data['Column'][i - 2]
        mask = _data['Mask'][i - 2]
        ts = _data['TestSite'][i - 2]

        file_path = f'{batch}\\{wafer}\\{date}\\{batch}_{wafer}_({row},{col})_{mask}_{ts}.png'
        cell = ws.cell(row=row_xl, column=col_xl, value='Click here to open image')  # Make display text

        # Style hyperlink
        cell.hyperlink = file_path
        cell.font = Font(color="0000FF", underline="single")
        i += 1

    # Save Excel file
    if __name__ == 'src.dataframe':
        wb.save('res\\result.xlsx')
    else:
        wb.save('..\\res\\result.xlsx')
