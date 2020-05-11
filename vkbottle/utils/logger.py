try:
    from loguru import logger
except ImportError:
    from .tools import Logger

    logger = Logger()


def loguru_installed():
    try:
        import loguru

        loguru_installed = True
    except ImportError:
        loguru_installed = False
    return loguru_installed
