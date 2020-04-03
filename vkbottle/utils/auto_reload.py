import os
import sys

from watchgod import awatch
from .logger import logger

_startup_cwd = os.getcwd()


def restart():
    """
    Author: https://github.com/cherrypy/cherrypy/blob/0857fa81eb0ab647c7b59a019338bab057f7748b/cherrypy/process/wspbus.py#L305
    :return:
    """
    args = sys.argv[:]
    logger.debug("Restarting: %s" % " ".join(args))
    args.insert(0, sys.executable)
    if sys.platform == "win32":
        args = ['"%s"' % arg for arg in args]

    os.chdir(_startup_cwd)
    os.execv(sys.executable, args)


async def _auto_reload(check_dir: str = "."):
    """
    Coro which see changes in your code and restart him.
    :return:
    """
    async for _ in awatch(check_dir):
        logger.info("Changes were found. Restarting...")
        restart()
