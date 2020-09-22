from abc import ABC, abstractmethod
from .views import ABCView
from .middlewares import BaseMiddleware
from typing import List, Dict, Callable, Type, NoReturn, Any
from vkbottle.api.abc import ABCAPI
from vkbottle.exception_factory.error_handler import ABCErrorHandler


class ABCRouter(ABC):
    """ Abstract Router
    Documentation: soon
    """

    views: Dict[str, "ABCView"] = {}
    middlewares: List["BaseMiddleware"]
    error_handler: "ABCErrorHandler"

    @abstractmethod
    async def route(self, event: dict, ctx_api: "ABCAPI"):
        pass

    @abstractmethod
    def construct(self, views: Dict[str, "ABCView"]) -> "ABCRouter":
        pass

    def add_view(self, name: str, view: "ABCView") -> NoReturn:
        self.views[name] = view

    def add_middleware(self, middleware: "BaseMiddleware") -> NoReturn:
        self.middlewares.append(middleware)

    def view(self, name: str) -> Callable[..., Type["ABCView"]]:
        def decorator(view: Type["ABCView"]):
            self.add_view(name, view())
            return view

        return decorator

    def middleware(self) -> Callable[..., Type["BaseMiddleware"]]:
        def decorator(middleware: Type["BaseMiddleware"]):
            self.add_middleware(middleware())
            return middleware

        return decorator
