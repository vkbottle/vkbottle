import logging.config

logging.config.fileConfig("configs/logging.ini")
_logger = logging.getLogger("bottle_logger")


class Logger:
    def __getattr__(self, item):
        if item in ("remove", "add", "level"):
            return lambda *args, **kwargs: None
        elif item == "success":
            return Logger()("info")
        return Logger()(item)

    def __call__(self, item, *args, **kwargs):
        return getattr(_logger, item)
