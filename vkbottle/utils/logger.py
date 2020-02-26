try:
    from loguru import logger
except ImportError:
    from .tools import Logger

    logger = Logger()
