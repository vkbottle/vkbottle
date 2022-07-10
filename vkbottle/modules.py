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


class Logger(Protocol):
    def info(self, msg, *args, **kwargs):
        ...

    def debug(self, msg, *args, **kwargs):
        ...

    def warning(self, msg, *args, **kwargs):
        ...

    def error(self, msg, *args, **kwargs):
        ...

    def critical(self, msg, *args, **kwargs):
        ...

    def exception(self, msg, *args, **kwargs):
        ...

    def log(self, level, msg, *args, **kwargs):
        ...


json: JSONModule = choice_in_order(
    ["ujson", "hyperjson", "orjson"], do_import=True, default="json"
)
logging_module = choice_in_order(["loguru"], do_import=True, default="logging")

if logging_module.__name__ == "loguru":
    logger: Logger = getattr(logging_module, "logger")  # type: ignore

elif logging_module.__name__ == "logging":
    import inspect

    class LogMessage:
        def __init__(self, fmt, args, kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return self.fmt.format(*self.args)

    class StyleAdapter(logging_module.LoggerAdapter):  # type: ignore
        def __init__(self, logger, extra=None):
            super().__init__(logger, extra or {})

        def log(self, level, msg, *args, **kwargs):
            if self.isEnabledFor(level):
                msg, args, kwargs = self.process(msg, args, kwargs)
                self.logger._log(level, msg, args, **kwargs)

        def process(self, msg, args, kwargs):
            log_kwargs = {
                key: kwargs[key]
                for key in inspect.getargspec(self.logger._log).args[1:]
                if key in kwargs
            }
            if isinstance(msg, str):
                msg = LogMessage(msg, args, kwargs)
                args = ()
            return msg, args, log_kwargs

    logger: Logger = StyleAdapter(logging_module.getLogger("vkbottle"))  # type: ignore

if hasattr(asyncio, "WindowsProactorEventLoopPolicy") and isinstance(
    asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy
):
    """
    This is a workaround for a bug in ProactorEventLoop:
    https://github.com/aio-libs/aiohttp/issues/4324

    This also can be fixed by using loop.run_until_complete instead of asyncio.run
    but I like to use asyncio.run because it's more readable.
    """
    from functools import wraps
    from asyncio.proactor_events import _ProactorBasePipeTransport, _ProactorBaseWritePipeTransport

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

    _ProactorBasePipeTransport.__del__ = silence_exception(_ProactorBasePipeTransport.__del__)
    _ProactorBaseWritePipeTransport._loop_writing = silence_exception(  # type: ignore
        _ProactorBaseWritePipeTransport._loop_writing  # type: ignore
    )
