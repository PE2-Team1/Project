import os


def get_lmz_path():
    dat_path = "..\\dat\\"

    batch_path = dat_path + os.listdir(dat_path)[0] + "\\"

    wafer_paths = [batch_path + wafer_path + "\\" for wafer_path in os.listdir(batch_path)]

    measure_date_paths = []
    for wafer_path in wafer_paths:
        for folder_name in os.listdir(wafer_path):
            if "." not in folder_name:
                measure_date_paths.append(wafer_path + folder_name + "\\")

    lmz_path = []
    for measure_date_path in measure_date_paths:
        for file_name in os.listdir(measure_date_path):
            if "LMZ" in file_name:
                lmz_path.append(file_name)
    print("Found LMZ data in dat folder: ")
    print(lmz_path)
    return lmz_path


if __name__ == "__main__":
    lmz_path = get_lmz_path()
