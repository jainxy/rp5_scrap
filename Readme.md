# rp5.in based Weather observation data download utility in python.

**Keep rp5Interface.py, logger.py, utils.py files together in the same directory**

## Pre-req - 
- Geckodriver => Needed fro selenium python module. Download from here - https://github.com/mozilla/geckodriver/releases
- selenium (We used Selenium Version - 3.141.0) python module
- requests python module
- Working FIREFOX browser (Most Important)

## Setup on Linux machine (optional) - 
run selenium_setup.sh to setup on linux machine
``` 
chmod +x ./selenium_setup.sh
./selenium_setup.sh
```

## Example Usage - 
1. download_script_basic.py -> A basic few-line script to test rp5Interface weather data download utility.
2. download_script_extended.py -> An extended script to test rp5Interface weather data download utility.

#### Mandatory arguments to rp5Interface.rp5_download API :
- location -> (string) Name of the place to download the weather data for.
- beginDate -> (string) Start Date in format - dd.mm.yyyy
- endDate -> (string) End Date in format - dd.mm.yyyy
- source -> (string) Data source from rp5.in portal. either "metar" or "archive". If wrong string is passed, 'archive' source will be chosen as fallback.

#### Optional arguments to rp5Interface.rp5_download API :
- FileName -> (string) Name of file without any extension
- dirPath -> (string) Full directory path where file is to be donwloaded. default - rp5_ddmmYYYY
- extract -> (bool) Weather to extract the downloaded .xls.gz file. Default - True