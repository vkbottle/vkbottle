import asyncio

from choicelib import choice_in_order
from typing_extensions import Protocol


class JSONModule(Protocol):
    def loads(self, s: str) -> dict:
        ...

    def dumps(self, o: dict) -> str:
        ...

    def load(self, f: str) -> dict:
        ...

    def dump(self, o: dict, f: str) -> None:
        ...


json: JSONModule = choice_in_order(
    ["ujson", "hyperjson", "orjson"], do_import=True, default="json"
)
logging_module = choice_in_order(["loguru"], default="logging")

if logging_module == "loguru":
    import os
    import sys

    if not os.environ.get("LOGURU_AUTOINIT"):
        os.environ["LOGURU_AUTOINIT"] = "0"
    from loguru import logger  # type: ignore

    if not logger._core.handlers:  # type: ignore
        log_format = (
            "<level>{level: <8}</level> | "
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{name}:{function}:{line} > <level>{message}</level>"
        )
        logger.add(sys.stderr, format=log_format, enqueue=True, colorize=True)

elif logging_module == "logging":
    """
    This is workaround for lazy formating with {} in logging.

    About:
    https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
    """
    import inspect
    import logging

    logging.basicConfig(level=logging.DEBUG)

    class LogMessage:
        def __init__(self, fmt, args, kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return self.fmt.format(*self.args)

    class StyleAdapter(logging.LoggerAdapter):
        def __init__(self, logger, extra=None):
            super().__init__(logger, extra or {})

        def log(self, level, msg, *args, **kwargs):
            if self.isEnabledFor(level):
                msg, args, kwargs = self.process(msg, args, kwargs)
                self.logger._log(level, msg, args, **kwargs)

        def process(self, msg, args, kwargs):
            log_kwargs = {
                key: kwargs[key]
                for key in inspect.getfullargspec(self.logger._log).args[1:]
                if key in kwargs
            }
            if isinstance(msg, str):
                msg = LogMessage(msg, args, kwargs)
                args = ()
            return msg, args, log_kwargs

    logger = StyleAdapter(logging.getLogger("vkbottle"))  # type: ignore
    logger.info(
        "logging is used as the default logger, but we recommend using loguru. "
        "It may also become a required dependency in future releases."
    )

if hasattr(asyncio, "WindowsProactorEventLoopPolicy") and isinstance(
    asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy  # type: ignore
):
    """
    This is a workaround for a bug in ProactorEventLoop:
    https://github.com/aio-libs/aiohttp/issues/4324

    This also can be fixed by using loop.run_until_complete instead of asyncio.run
    but I like to use asyncio.run because it's more readable, and not require to create new event loop.
    """
    from asyncio.proactor_events import _ProactorBasePipeTransport, _ProactorBaseWritePipeTransport
    from functools import wraps

    def silence_exception(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (AttributeError, RuntimeError) as e:
                if str(e) not in (
                    "'NoneType' object has no attribute 'send'",
                    "Event loop is closed",
                ):
                    raise

        return wrapper

    _ProactorBasePipeTransport.__del__ = silence_exception(_ProactorBasePipeTransport.__del__)  # type: ignore
    _ProactorBaseWritePipeTransport._loop_writing = silence_exception(  # type: ignore
        _ProactorBaseWritePipeTransport._loop_writing  # type: ignore
    )
