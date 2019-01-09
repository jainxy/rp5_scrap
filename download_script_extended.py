# This is an extended script to test rp5Interface weather data download utility
# see 'download_script_basic.py' for basic example.

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
    from rp5Interface import rp5_download
    parser = argparse.ArgumentParser("Waether Data downloading script's arguments")
    parser._action_groups.pop()

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    # Required Arguments
    required_args.add_argument("-l", "--loc", required=True, help = "(string) Name of the place to download the weather data for")
    required_args.add_argument("-b", "--begin_date", required=True, help="(string) Start Date in format - dd.mm.yyyy")
    required_args.add_argument("-e", "--end_date", required=True, help="(string) End Date in format - dd.mm.yyyy")
    required_args.add_argument("-s", "--source", required=True, help="(string) Data source from rp5.in portal. either 'metar' or 'archive'. \
                      If wrong string is passed, 'archive' source will be chosen as fallback.")

    # Optional Arguments
    optional_args.add_argument("-f", "--file_name", default=None, help = "(string) Name of file without any extension")
    optional_args.add_argument("-d", "--dir_path", default=None, help = "(string) Full directory path where file is to be donwloaded. default - rp5_ddmmYYYY")
    optional_args.add_argument("--extract", default=True, help = "(bool) Weather to extract the downloaded .xls.gz file. Default - True")

    args = parser.parse_args()

    rp5_download(location=args.loc, beginDate=args.begin_date, endDate=args.end_date, source=args.source, fileName=args.file_name, \
                 dirPath=args.dir_path, extract = args.extract)


if __name__ == "__main__":
    main()