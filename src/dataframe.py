import pandas as pd
import xml.etree.ElementTree as ET

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
    'Analysis Wavelength': [],
    'Rsq of Ref. spectrum (Nth)': [],
    'Max transmission of Ref. spectrum (dBm)': [],
    'Rsq of IV': [],
    'I at -1V (A)': [],
    'I at +1V (A)': [],
}


def add_dict(new_dict):
    global data
    for key in new_dict.keys():
        data[key].append(new_dict[key])


def make_new_data(lmz_path, info, iv, trans):
    root = ET.parse(lmz_path).getroot()
    test_site_info = root.find('.//TestSiteInfo').attrib
    date = root.find('.//PortCombo').attrib['DateStamp']
    new_data = {
        'Batch': test_site_info['Batch'],
        'Wafer': test_site_info['Wafer'],
        'Mask': test_site_info['Maskset'],
        'TestSite': test_site_info['TestSite'],
        'Name': root.find('.//Modulator').attrib['Name'],
        'Date': date,
        'Script ID': info['script_id'],
        'Script Version': info['script_version'],
        'Script Owner': info['script_owner'],
        'Operator': info['operator_name'],
        'Row': test_site_info['DieRow'],
        'Column': test_site_info['DieColumn'],
        'Error Flag': "",
        'Error Desc.': "",
        'Analysis Wavelength': [],
        'Rsq of Ref. spectrum (Nth)': [],
        'Max transmission of Ref. spectrum (dBm)': [],
        'Rsq of IV': iv['R_squared'],
        'I at -1V (A)': iv['abs_current'][4],
        'I at +1V (A)': iv['abs_current'][12],
    }
    return new_data


def export(_data):
    df = pd.DataFrame(_data)
    if __name__ == 'src.dataframe':
        df.to_csv('res\\result.csv', index=False)
    else:
        df.to_csv('..\\res\\result.csv', index=False)
