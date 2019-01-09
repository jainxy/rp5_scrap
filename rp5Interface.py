import os
import sys
import selenium
import time
import gzip
import shutil

import utils

from logger import Log
from utils import DataSource, download_data

from selenium import webdriver

class RP5Interface(object):
    URL = "http://rp5.in/"

    def __init__(self, location, beginDate, endDate, source, fileName=None, dirPath=None):
        Log.info("Selenium Version - {}".format(selenium.__version__))
        self._loc = location
        self._beginDate = beginDate
        self._endDate = endDate
        self._exit_msg = ""
        self._rp5source = source
        self._fileName = fileName
        self._dirPath=dirPath
        self._browser = None

    def _browser_create(self):
        try:
            if self._browser is not None:
                Log.info("Closing Existing browser instance")
                self._browser.close()
            self._browser=webdriver.Firefox()
            Log.info("Creating browser instance ...")
        except:
            Log.fatal("Some error occured while creating browser instance!")

    def _browser_exit(self, exit_status=0):
        if self._browser is not None:
            self._browser.close()
            if exit_status is not 0:
                Log.error(self._exit_msg)
            else:
                Log.info(self._exit_msg)
            sys.exit(exit_status)

    def _search_loc(self):
        if self._browser is not None:
            self._browser.get("http://rp5.in/")

            searchElem = self._browser.find_element_by_id('searchStr')
            searchElem.clear()
            Log.info("Searching for location - {}".format(self._loc))
            searchElem.send_keys(self._loc)

            searchButtonElem = self._browser.find_element_by_id('searchButton')
            searchButtonElem.click()

            try:
                self._browser.find_element_by_class_name('searchResults')
            except selenium.common.exceptions.NoSuchElementException:
                self._exit_msg = "No Search results, Pls try searching with other location"
                self._browser_exit(1)
            except:
                self._exit_msg = "some other error happened while searching"
                self._browser_exit(1)

    def _select_loc(self):
        if self._browser is not None:
            searchTextElem1 = self._browser.find_elements_by_xpath("//tr[@class='srow0']")
            searchTextElem2 = self._browser.find_elements_by_xpath("//tr[@class='srow1']")
            searchTextElem = searchTextElem1 + searchTextElem2

            for webElement in searchTextElem:
                searchText = webElement.text
                if (searchText.lower().find("india") == -1):
                    if (webElement == searchTextElem[-1]):
                        self._exit_msg = "Search result is outside of India, Pls try searching with a location in India"
                        self._browser_exit(1)
                    else:
                        continue
                else:
                    break
            locElem = webElement.find_element_by_tag_name('a')
            locElem.click()

    def _select_data_source(self):
        if self._browser is not None:
            if (self._rp5source.lower() == "metar"):
                Log.info("Getting METAR data")
                dataLinkElem = self._browser.find_element_by_id('metar_link')
            elif (self._rp5source.lower() == "archive"):
                Log.info("Getting ARCHIVE data")
                dataLinkElem = self._browser.find_element_by_id('archive_link')
            else:
                self._exit_msg = "Something went wrong, exiting!"
                self._browser_exit(1)
            dataLinkElem.click()

    def download_date(self):
        self._browser_create()
        self._search_loc()
        self._select_loc()

        DataSource.setSource(self._rp5source)
        self._rp5source = DataSource.getSource()

        self._select_data_source()

        if (self._rp5source.lower() == "metar"):
            downTabElem = self._browser.find_element_by_id('tabMetarDLoad')
        elif (self._rp5source.lower() == "archive"):
            downTabElem = self._browser.find_element_by_id('tabSynopDLoad')
        else:
            self._exit_msg = "Rp5 Source is not from available options, pls retry, exiting!"
            self._browser_exit(1)
        downTabElem.click()
        time.sleep(3)

        beginDateElem = self._browser.find_element_by_id('calender_dload')
        beginDateElem.clear()
        Log.info("Start Date is - {}".format(self._beginDate))
        beginDateElem.send_keys(self._beginDate)

        endDateElem = self._browser.find_element_by_id('calender_dload2')
        endDateElem.clear()
        Log.info("End Date is - {}".format(self._endDate))
        endDateElem.send_keys(self._endDate)

        generateDownloadElem = self._browser.find_elements_by_class_name('archButton')[1]
        generateDownloadElem.click()
        time.sleep(5)

        try:
            downloadElem = self._browser.find_element_by_link_text('Download')
            fileUrl = downloadElem.get_attribute('href')
            Log.info("File URL is - " + fileUrl)
        except:
            self._exit_msg = "Download link not found, exiting ..."
            self._browser_exit(1)

        fullPath = download_data(fileUrl,self._fileName,self._dirPath)
        Log.info("Downloading Data to {} ...".format(fullPath))

        Log.info("rp5 data downloaded successfully for {} location from {} to {}".format(self._loc,self._beginDate,self._endDate))
        self._browser.close()
        return fullPath

def rp5_download(location, beginDate, endDate, source, fileName = None, dirPath = None, extract = True):

    # Mandatory arguments to rp5Interface.rp5_download API :
    #    location -> (string) Name of the place to download the weather data for.
    #    beginDate -> (string) Start Date in format - dd.mm.yyyy
    #    endDate -> (string) End Date in format - dd.mm.yyyy
    #    source -> (string) Data source from rp5.in portal. either "metar" or "archive"

    # Optional arguments to rp5Interface.rp5_download API :
    #   FileName -> (string) Name of file without any extension
    #   dirPath -> (string) Full directory path where file is to be donwloaded. default - rp5_ddmmYYYY
    #   extract -> (bool) Weather to extract the downloaded .xls.gz file. Default - True

    if fileName is not None:
        fileName = fileName + '.xls.gz'
    rp5 = RP5Interface(location=location,beginDate=beginDate,endDate=endDate,source=source,fileName=fileName,dirPath=dirPath)
    fullPath = rp5.download_date()
    if extract:
        fileFullPath = fullPath.rsplit('.',1)[0]
        with gzip.open(fullPath,'rb') as f_in:
            with open(fileFullPath, 'wb') as f_out:
                shutil.copyfileobj(f_in,f_out)
                Log.info("Extracted file at - {}".format(fileFullPath))


