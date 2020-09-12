try:
    from loguru import logger
except ImportError:
    from ._custom_logger import Logger

    logger = Logger()
