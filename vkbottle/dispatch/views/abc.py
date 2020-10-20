from abc import ABC, abstractmethod
from typing import Any, List

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.dispatch.return_manager import BaseReturnManager
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser


class ABCView(ABC):
    handlers: List["ABCHandler"]
    middlewares: List["BaseMiddleware"]
    handler_return_manager: BaseReturnManager

    @abstractmethod
    async def process_event(self, event: dict) -> bool:
        pass

    @abstractmethod
    async def handle_event(
        self, event: dict, ctx_api: "ABCAPI", state_dispenser: "ABCStateDispenser"
    ) -> Any:
        pass

    def register_middleware(self, middleware: "BaseMiddleware"):
        self.middlewares.append(middleware)
