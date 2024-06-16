# LMZ processor
Processes data from Lumped Mach-Zehnder Modulators

Made by Team 1

## Introduction
The Program is a tool for analyzing and visualizing the characteristics of semiconductor wafer devices. This program allows users to easily measure and analyze various electrical properties of wafers.

## key Features
- Measurement of electrical properties of wafer devices
- Data visualization and graph generation
- Data analysis and excel file generation

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

Scripts below should be executed from `run.py`.
- `get_lmz_path.py` 
  - Be ran once to get XML file paths. 
  - Also creates directories in `res` folder. 
- `operate.py`
  - Executes main process and loops for all XML data.
- `vi_process.py`
  - Gets Current-Voltage data and performs polynomial fitting. 
- `trans_process.py`
  - Gets transmission spectra + reference and performs reference fitting.
  - `trans_process2.py` supports transmission flattening. 
- `plot_figure.py`
  - Plots transmission spectra, fitted reference, flattened transmission and I-V characteristics.
  - Saves plot image in `res` folder.
- `dataframe.py`
  - Aggregates process results and outputs to an Excel file in `res` folder.

## How to install and run

- #### Requirements

```
pandas>=2.1.4
numpy>=1.26.4
lmfit>=1.2.2
matplotlib>=3.8.0
scipy>=1.11.4
openpyxl>=3.0.10
```
**Step 1:** Install requirements

For pip:
```shell
$ pip install pandas numpy lmfit matplotlib scipy openpyxl
```

For Anaconda: 
```shell
$ conda install pandas numpy lmfit matplotlib scipy openpyxl
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

**Step 4:** Run `run.py`

**Step 5** Check process results in `res` folder

## Troubleshooting
- Issue: The program won't start.
  - Solution: Ensure all dependencies are installed and Python is correctly set up.
- Issue: Data file not recognized. 
  - Solution: Verify that the data file is in the correct format and located in the data/ directory.

## FAQ
- <span style="font-size: 1.2em;"> Q:</span> An error occurs when I run the program. How can I fix it?
- <span style="font-size: 1.2em;"> A:</span> First, check that all dependencies are installed and that your Python version meets the requirements. If the problem persists, contact us via email.

<br>

- <span style="font-size: 1.2em;"> Q:</span> Can I export the data analysis results in different formats?
- <span style="font-size: 1.2em;"> A:</span> Yes, data analysis results can be exported in various formats, such as CSV, and Excel.

## Made by:

#### -Kim Beomseo
#### -Son Eunji
#### -Lee Hyeonseok
 


## Contact Email
If you have any questions or inquiries, please contact us via email.

| name     | email                |
|----------|----------------------|
| Lee hyeonseok | hs7681@hanyang.ac.kr |
| Kim Bumseo | eunjeeok2@naver.com  |
|  Son Eunji         | kbs03@hanyang.ac.kr  |
