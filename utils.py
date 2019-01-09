import os
import requests
import datetime

from logger import Log

def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def download_data(fileUrl,dirPath = None,fileName = None):
    res = requests.get(fileUrl)
    res.raise_for_status()
    current_date = datetime.datetime.today().strftime("%d%m%Y")
    if fileName is None:
        fileName = 'rp5.in_'+current_date+'_'+fileUrl.rsplit('/',1)[1]
    if dirPath is None:
        dirPath = 'rp5_'+current_date
        make_dir(dirPath)
    else:
        make_dir(dirPath)
    with open(os.path.join(dirPath, fileName), "wb") as code:
        code.write(res.content)
    return os.path.join(dirPath,fileName)


class DataSource(object):
    class __SOURCES:
        ARCHIVE = "ARCHIVE" ; METAR = "METAR"
    __source = __SOURCES.ARCHIVE   # Default source of data

    @classmethod
    def setSource(cls,sourceStr):
        cls.__source = getattr(cls.__SOURCES, sourceStr.upper(), cls.__SOURCES.ARCHIVE)
        Log.info("Setting Data source as {}".format(cls.__source))

    @classmethod
    def getSource(cls):
        return cls.__source

    @classmethod
    def get_supported_sources(cls):
        return [cls.__SOURCES.ARCHIVE, cls.__SOURCES.METAR]