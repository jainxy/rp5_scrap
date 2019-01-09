import sys
from datetime import datetime


class TerminalColor:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Log(object):
    class LEVELS:
        ALL, TRACE, DEBUG, INFO, WARNING, ERROR, FATAL = range(7)

    _LEVEL = LEVELS.INFO

    @staticmethod
    def set_level(levelstr):
        try:
            level = getattr(Log.LEVELS, levelstr.upper())
            Log._LEVEL = level
        except AttributeError:
            Log.fatal("invalid log level {}".format(levelstr))

    @staticmethod
    def get_levels():
        return ["ALL", "TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "FATAL"]

    @staticmethod
    def fatal(msg):
        if Log._LEVEL <= Log.LEVELS.FATAL:
            Log._log("[FATAL] " + str(msg), TerminalColor.RED)
            sys.exit(1)

    @staticmethod
    def error(msg):
        if Log._LEVEL <= Log.LEVELS.ERROR:
            Log._log("[ERROR] " + str(msg), TerminalColor.RED)

    @staticmethod
    def warning(msg):
        if Log._LEVEL <= Log.LEVELS.WARNING:
            Log._log("[WARNING] " + str(msg), TerminalColor.YELLOW)

    @staticmethod
    def info(msg):
        if Log._LEVEL <= Log.LEVELS.INFO:
            Log._log("[INFO] " + str(msg), TerminalColor.GREEN)

    @staticmethod
    def debug(msg):
        if Log._LEVEL <= Log.LEVELS.DEBUG:
            Log._log("[DEBUG] " + str(msg), TerminalColor.WHITE)

    @staticmethod
    def trace(msg):
        if Log._LEVEL <= Log.LEVELS.TRACE:
            Log._log("[TRACE] " + str(msg), TerminalColor.WHITE)

    @staticmethod
    def _log(msg, color=TerminalColor.WHITE):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("{} - {}{}{}".format(cur_time, color, msg, TerminalColor.WHITE))