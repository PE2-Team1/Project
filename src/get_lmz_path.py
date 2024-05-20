import os


def get_lmz_path(wafer, device):
    if __name__ == "__main__":
        dat_path = "..\\dat\\"
    else:
        dat_path = "dat\\"

    batch_path = dat_path + os.listdir(dat_path)[0] + "\\"

    if not wafer:
        wafer = os.listdir(batch_path)
    wafer_paths = [batch_path + wafer_path + "\\" for wafer_path in wafer]

    measure_date_paths = []
    for wafer_path in wafer_paths:
        for folder_name in os.listdir(wafer_path):
            if "." not in folder_name:
                measure_date_paths.append(wafer_path + folder_name + "\\")

    lmz_path = []
    for measure_date_path in measure_date_paths:
        for file_name in os.listdir(measure_date_path):
            if any(d in file_name for d in device):
                if __name__ == "__main__":
                    lmz_path.append(measure_date_path + file_name)
                else:
                    lmz_path.append('..\\' + measure_date_path + file_name)
    print(f"Found {len(lmz_path)} LMZ data in dat folder: ")
    print(lmz_path)
    return lmz_path


if __name__ == "__main__":
    get_lmz_path([], ['LMZC', 'LMZO'])
