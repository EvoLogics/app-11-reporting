# Library imports.
from colorama import Fore, Style
from datetime import datetime
from enum import IntEnum


# Report type enum
class LogLevel(IntEnum):
    Debug       = 0
    Normal      = 1
    Quiet       = 2

    def __str__(self):
        return self.name.upper()


class Logger:
    _instance = None
    _name = None
    _log_level = LogLevel.Normal

    def __new__(cls, name):
        if cls._name is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._name = name
        return cls._instance

    def log(self, message="", debugLevel="INFO", color=Fore.WHITE):
        print("{}[{}][{:7s}] {}{}".format(
                                      color,
                                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      debugLevel,
                                      message,
                                      Style.RESET_ALL))

    def setLogLevel(self, logLevel):
        self._log_level = logLevel

    def debug(self, message=""):
        if self._log_level <= LogLevel.Debug:
          self.log(message, "DEBUG", Fore.CYAN)

    def info(self, message=""):
        if self._log_level <= LogLevel.Normal:
            self.log(message, "INFO")

    def warning(self, message=""):
        if self._log_level <= LogLevel.Normal:
            self.log(message, "WARNING", Fore.YELLOW)

    def error(self, message=""):
        if self._log_level <= LogLevel.Quiet:
            self.log(message, "ERROR", Fore.RED)

    def success(self, message=""):
        if self._log_level <= LogLevel.Quiet:
            self.log(message, "SUCCESS", Fore.GREEN)


log = Logger("APP-11")

def debug(message):
    log.debug(message)

def info(message):
    log.info(message)

def warning(message):
    log.warning(message)

def error(message):
    log.error(message)

def success(message=""):
    log.success(message)
