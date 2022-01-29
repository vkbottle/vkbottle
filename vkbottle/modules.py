import logging

from choicelib import choice_in_order
from typing_extensions import Protocol


class JSONModule(Protocol):
    def loads(self, s: str) -> dict:
        ...

    def dumps(self, o: dict) -> str:
        ...


json: JSONModule = choice_in_order(
    ["ujson", "hyperjson", "orjson"], do_import=True, default="json"
)
logger = choice_in_order(["loguru"], do_import=True, default="logging")

if logger.__name__ == "logging":
    logger = logging.getLogger("vkbottle")
elif logger.__name__ == "loguru":
    logger = getattr(logger, "logger")
