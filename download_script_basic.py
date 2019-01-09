# This is a basic few-line script to test rp5Interface weather data download utility
# Requirements - rp5Interface.py, logger.py, utils.py files together into same directory
#               - selenium (We used Selenium Version - 3.141.0) python module
#               - requests python module
#               - geckodriver (We used v0.23); run selenium_setup.sh to setup on linux machine
#               - Working FIREFOX browser

# Mandatory arguments to rp5Interface.rp5_download API :
#    location -> (string) Name of the place to download the weather data for.
#    beginDate -> (string) Start Date in format - dd.mm.yyyy
#    endDate -> (string) End Date in format - dd.mm.yyyy
#    source -> (string) Data source from rp5.in portal. either "metar" or "archive".
#                       If wrong string is passed, 'archive' source will be chosen as fallback.

# Optional arguments to rp5Interface.rp5_download API :
#   FileName -> (string) Name of file without any extension
#   dirPath -> (string) Full directory path where file is to be donwloaded. default - rp5_ddmmYYYY
#   extract -> (bool) Weather to extract the downloaded .xls.gz file. Default - True

# See below command for basic usage

import os
import subprocess
import argparse
import sys
import datetime
import time

from rp5Interface import rp5_download

def main():
    rp5_download(location="bengaluru",beginDate="1.12.2018",endDate="7.01.2019",source="metar")

if __name__ == "__main__":
    main()
