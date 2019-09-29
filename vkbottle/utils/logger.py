"""Read LICENSE.txt"""

"""
FILE WITH LOGGERS AND LOG-FEATURES
"""

import re
import time
from ..project_collections import colored, ANSIColor


class Logger:
    """Coloring class, engine of all debug messages and warns
    """
    def __init__(self, debug):
        self.debug = debug

    async def __call__(self, *text, separator=' '):
        if self.debug is True:
            new = ''
            for i, el in enumerate(text):
                new += str(el)
                if i + 1 != len(text):
                    new += separator
            print("[" + colored('VKBottle', 'blue') + "] " + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), new) + ANSIColor.RESET)

    async def warn(self, *text, separator=' '):
        if self.debug is True:
            new = ''
            for i, el in enumerate(text):
                new += str(el)
                if i + 1 != len(text):
                    new += separator
            print("[" + colored('VKBottle WARN', 'blue') + "] " + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), new) + ANSIColor.RESET)

    @staticmethod
    async def error(*text, separator=' '):
        new = ''
        for i, el in enumerate(text):
            new += str(el)
            if i + 1 != len(text):
                new += separator
        print("[" + colored('VKBottle ERROR', 'blue') + "] " + re.sub('#', time.strftime("%m-%d %H:%M:%S", time.gmtime()), new) + ANSIColor.RESET)

    async def progress_bar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
        if self.debug is True:
            prefix = "[" + colored('VKBottle ERROR', 'blue') + "] " + prefix
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)

            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
            # Print New Line on Complete
            if iteration == total:
                print()