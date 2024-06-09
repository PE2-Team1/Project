# LMZ processor
Process data from Lumped Mach-Zehnder Modulators

Made by Team 1

## How it works
### Directories
- `dat`
  - Data to be analyzed are put here.
- `doc`
  - Jupyter notebook file for analysis visualization is here.
- `ppt`
  - The final presentation PPT file is here.
- `res`
  - Resultant plot images and Excel file are saved here.
- `src`
  - Scripts are placed here.

### Scripts
- `run.py`
  - Includes script informations and run options.

Scripts below should be executed from `run.py`.
- `get_lmz_path.py` 
  - Be ran once to get XML file paths. 
  - Also creates directories in `res` folder. 
- `operate.py`
  - Executes main process and loops for all XML data.
- `vi_process.py`
  - Gets Current-Voltage data and performs polynomial fitting. 
- `trans_process.py`
  - Gets transmission spectra + reference and performs reference fitting and transmission flattening. 
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

File structure must be like below:
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

