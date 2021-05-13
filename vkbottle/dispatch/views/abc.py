from abc import ABC, abstractmethod
from typing import Any, List

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.dispenser.abc import ABCStateDispenser
from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.middlewares import BaseMiddleware
from vkbottle.dispatch.return_manager import BaseReturnManager


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

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"handlers={self.handlers} "
            f"middlewares={self.middlewares} "
            f"handler_return_manager={self.handler_return_manager}"
        )
