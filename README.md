# LMZ processor
Process data from Lumped Mach-Zehnder Modulators

Made by team 1


## How to install and run

- ### Requirements

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

**Step 2:** Put LMZ measurement XML data into ```dat``` folder

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

**Step 3:** Open ```run.py``` and configure options

**Step 4:** Run ```run.py```

**Step 5** Check process results in ```res``` folder

