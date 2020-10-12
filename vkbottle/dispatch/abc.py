from abc import ABC, abstractmethod
from .views import ABCView
from .middlewares import BaseMiddleware
from typing import Dict, Callable, Type, NoReturn
from vkbottle.api.abc import ABCAPI
from vkbottle.exception_factory.error_handler import ABCErrorHandler


class ABCRouter(ABC):
    """ Abstract Router
    Documentation: soon
    """

    views: Dict[str, "ABCView"] = {}
    error_handler: "ABCErrorHandler"

    @abstractmethod
    async def route(self, event: dict, ctx_api: "ABCAPI"):
        pass

    @abstractmethod
    def construct(self, views: Dict[str, "ABCView"]) -> "ABCRouter":
        pass

    def add_view(self, name: str, view: "ABCView") -> NoReturn:
        self.views[name] = view

    def view(self, name: str) -> Callable[..., Type["ABCView"]]:
        def decorator(view: Type["ABCView"]):
            self.add_view(name, view())
            return view

        return decorator
