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

    class LogMessage:
        def __init__(self, fmt, args):
            self.fmt = fmt
            self.args = args

        def __str__(self):
            return self.fmt.format(*self.args)

    class StyleAdapter(logging_module.LoggerAdapter):  # type: ignore
        def __init__(self, logger, extra=None):
            super().__init__(logger, extra or {})

        def log(self, level, msg, /, *args, **kwargs):
            if self.isEnabledFor(level):
                msg, kwargs = self.process(msg, kwargs)
                self.logger._log(level, LogMessage(msg, args), (), **kwargs)

    logger: Logger = StyleAdapter(logging_module.getLogger("vkbottle"))  # type: ignore
