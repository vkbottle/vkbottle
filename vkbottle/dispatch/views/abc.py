from abc import ABC, abstractmethod
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware
from typing import Any, List


class ABCView(ABC):
    handlers: List["ABCHandler"]
    middleware: List["BaseMiddleware"]

    @abstractmethod
    async def process_event(self, event: dict) -> bool:
        pass

    @abstractmethod
    async def handle_event(self, event: dict) -> Any:
        pass
