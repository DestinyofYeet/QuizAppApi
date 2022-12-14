import os
import pathlib
import sys
import traceback as tb_module

from datetime import datetime
from colorama import Style
from threading import Lock
from api.utils.meta.singleton import Singleton

from api.utils.logger.error_levels import WarningLevel, DebugLevel
from api.utils.logger.error_levels import ErrorLevel, Level, InfoLevel


class Logger(metaclass=Singleton):
    def __init__(self, where_to_log_file: str = "", only_print_over_and_including_severity=InfoLevel.InfoLevel(), file_name="app.log"):
        self.__where_to_log_file__: str = where_to_log_file
        self.__only_print_over_and_including_severity__ = only_print_over_and_including_severity
        self.__file_name__ = file_name

        sys.excepthook = self.custom_sys_except_hook

        self.__log_path__ = str(pathlib.Path(__file__).parent.parent.parent.parent.absolute()) + "/" + self.__where_to_log_file__

        self.__lock__ = Lock()

        if self.__where_to_log_file__:
            if not os.path.exists(self.__log_path__):
                os.mkdir(self.__log_path__)

            if os.path.exists(self.__log_path__ + f"/{self.__file_name__}.old"):
                os.remove(self.__log_path__ + f"/{self.__file_name__}.old")

            if os.path.exists(self.__log_path__ + f"/{self.__file_name__}"):
                os.rename(self.__log_path__ + f"/{self.__file_name__}", self.__log_path__ + f"/{self.__file_name__}.old")

    @staticmethod
    def __get_format__() -> str:
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def __print_message__(self, level: Level.Level, message):
        if level.severity_number >= self.__only_print_over_and_including_severity__.severity_number:
            print(f"{level.color}[{level.severity}] {self.__get_format__()}: {message}{Style.RESET_ALL}")

        if self.__where_to_log_file__:
            with open(self.__log_path__ + f"/{self.__file_name__}", "a") as f:
                f.write(f"[{level.severity}] {self.__get_format__()}: {message}\n")

    def debug(self, message):
        with self.__lock__:
            self.__print_message__(
                level=DebugLevel.DebugLevel(),
                message=message
            )

    def info(self, message):
        with self.__lock__:
            self.__print_message__(
                level=InfoLevel.InfoLevel(),
                message=message
            )

    def warning(self, message):
        with self.__lock__:
            self.__print_message__(
                level=WarningLevel.WarningLevel(),
                message=message
            )

    def error(self, message):
        with self.__lock__:
            self.__print_message__(
                level=ErrorLevel.ErrorLevel(),
                message=message
            )

    def custom_sys_except_hook(self, exctype, value, traceback):
        error = "".join(tb_module.format_exception(exctype, value, traceback))
        self.error(f"{exctype.__name__} was raised with error: {value}\n{error}")
        sys.__excepthook__(exctype, value, traceback)
