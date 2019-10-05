import logging
from logging import handlers
from typing import Any
from termcolor import colored
from colorama import init as color_opt
import re
import time


LOG_FILE_PATTERN = r'[a-zA-Z0-9]+\.log'
DEFAULT_LOG_NAME = 'bot.log'
LOG_FORMAT = '[%(asctime)s %(name)s - %(levelname)s] - %(message)s'


class Coloring(object):
    def __init__(self):
        color_opt()
        self.prefix = '[' + colored('VKBottle', 'blue') + ']'

    def __call__(self, text: str, color: str = 'white') -> colored:
        return '{prefix} {text}'.format(prefix=self.prefix,
                                        text=colored(text.replace('#', time.strftime("%m-%d %H:%M:%S", time.gmtime())), color))


class Logger(object):
    def __init__(self,
                 debug: bool,
                 log_file: str,
                 plugin_folder: str,
                 level=None,
                 logger_name: str = None):

        self.__debug: bool = debug
        self.__coloring = Coloring()
        self.__level = level or logging.DEBUG
        self.logger = logging.getLogger(logger_name or 'VKBottle')

        log_path = '{path}/{log_file}'.format(
            path=plugin_folder,
            log_file=log_file if log_file and re.match(LOG_FILE_PATTERN, log_file) else DEFAULT_LOG_NAME)

        open(log_path, 'w+').close()
        self.logger.setLevel(self.__level)
        formatter = logging.Formatter(LOG_FORMAT)

        handler = handlers.WatchedFileHandler(log_path)
        handler.setLevel(self.__level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.debug('My logging file path is {}'.format(log_path))

    def info(self, *some: Any):
        self.logger.info(*some)

    def debug(self, *some):
        self.logger.debug(*some)
        if self.__debug:
            print(self.__coloring(' '.join([str(i) for i in some])))

    def mark(self, *some):
        self.logger.debug(*some)
        if self.__debug:
            print(self.__coloring(' '.join([str(i) for i in some]), 'grey'))

    def warning(self, *some):
        self.logger.debug(*some)
        if self.__debug:
            print(self.__coloring(' '.join([str(i) for i in some]), 'yellow'))

    def error(self, *some):
        self.logger.debug(*some)
        if self.__debug:
            print(self.__coloring(' '.join([str(i) for i in some]), 'red'))
