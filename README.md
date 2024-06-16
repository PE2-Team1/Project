# LMZ processor
Processes data from Lumped Mach-Zehnder Modulators

Made by Team 1: Kim Beomseo, Son Eunji, Lee Hyeonseok

## Introduction
This program is a tool for analyzing and visualizing the characteristics of multiple LMZ devices.

## Key Features
- Automated analysis of electrical/optical properties of LMZ devices.
- Data visualization.
- Raising flags for unexpected values (low fit result, low transmission).
- Exporting analysis results to an Excel file.

## How it works
### Directories
- `dat`
  - Data to be analyzed are put here.
- `doc`
  - Jupyter notebook file for analysis visualization is here.
- `res`
  - Resultant plot images and Excel file are saved here.
- `src`
  - Scripts are placed here.

### Scripts
- `run.py`
  - Includes script information and run options.
  
  - ```python
    # ------ Info & Options ------ #
    info = {
      'script_id': "Process LMZ",
        'script_owner': 'Team 1',
        'script_version': 0.1,
        'operator_name': "", # Put your name here
    }
    wafer = []  # ['D07', 'D08', ...]. Blank out list to process all wafers
    device = ['LMZC', 'LMZO'] 
    save_figure = False # save figures in res folder
    export_excel = True # save analysis result as an Excel file

Scripts below must be executed from `run.py`.
- `get_lmz_path.py` 
  - Be ran once to get XML file paths. 
  - Also creates directories in `res` folder. 
- `operate.py`
  - Executes main process and loops for all XML data.
- `vi_process.py`
  - Gets Current-Voltage data and performs polynomial fitting. 
- `trans_process.py`
  - Gets transmission spectra + reference. Performs reference fitting and transmission flattening.
- `plot_figure.py`
  - Plots transmission spectra, fitted reference, flattened transmission and I-V characteristics.
  - Saves plot images in `res` folder.
- `dataframe.py`
  - Aggregates process results and outputs to an Excel file in `res` folder.

## How to install and run

- #### Requirements

```
pandas
numpy
lmfit
matplotlib
scipy
openpyxl
ipywidgets
IPython
```
**Step 1:** Install requirements

For pip:
```shell
$ pip install -r requirements.txt
```

For Anaconda: 
```shell
$ conda install -r requirements.txt
```

**Step 2:** Put LMZ measurement XML data into `dat` folder

File structure must be like below (currently supports for only 1 Batch folder):
```
dat/
└── Batch/
    ├── Wafer1/
    │   ├── Measure_date1/
    │   │   └── data1.xml
    │   │   └── data2.xml
    │   │   └── data3.xml
    │   │   └── ...
    │   ├── Measure_date2/
    │   │   └── data1.xml
    │   │   └── ...
    │   ├── ...
    │
    │
    ├── Wafer2/
    │   ├── Measure_date1/
    │   │   └── data1.xml
    │   ├── Measure_date2/
    │   │   └── data1.xml
    │   ├── ...
    │
    │
    ├── ...
```

**Step 3:** Open `run.py` and configure options

Check script descriptions!

**Step 4:** Run `run.py`

It may take 3-5 minutes for processing 100 data

**Step 5** Check process results in `res` folder

## Troubleshooting
- Issue: The program does not start.
  - Solution: Ensure all dependencies are installed and Python is correctly set up.
- Issue: Data file not recognized. 
  - Solution: Verify that the data file is in the correct format and located in the dat/ directory.





## Contact Email
If you have any questions or inquiries, please contact us via email.

| name          | email                |
|---------------|----------------------|
| Lee Hyeonseok | hs7681@hanyang.ac.kr |
| Kim Beomseo   | kbs03@hanyang.ac.kr  |
| Son Eunji     |  eunjeeok2@naver.com |
