from abc import ABC, abstractmethod
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.api.abc import ABCAPI
from typing import Any, List


class ABCView(ABC):
    handlers: List["ABCHandler"]
    middlewares: List["BaseMiddleware"]

    @abstractmethod
    async def process_event(self, event: dict) -> bool:
        pass

    @abstractmethod
    async def handle_event(self, event: dict, ctx_api: "ABCAPI") -> Any:
        pass
