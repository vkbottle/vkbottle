from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    List,
    NoReturn,
    Optional,
    TypeVar,
    overload,
)

if TYPE_CHECKING:
    from vkbottle.dispatch.handlers.abc import ABCHandler
    from vkbottle.dispatch.views.abc import ABCView


T = TypeVar("T")


class MiddlewareError(Exception):
    pass


class ABCMiddleware(ABC):
    @abstractmethod
    def stop(self, description: Any = "") -> NoReturn:
        ...

    @overload
    @abstractmethod
    async def pre(self) -> None:
        ...

    @overload
    @abstractmethod
    async def pre(self, context_variables: Optional[dict] = None) -> None:
        ...

    @overload
    @abstractmethod
    async def post(self) -> None:
        ...

    @overload
    @abstractmethod
    async def post(self, context_variables: Optional[dict] = None) -> None:
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class BaseMiddleware(Generic[T]):
    event: T
    view: Optional["ABCView"]
    handle_responses: List
    handlers: List["ABCHandler"]

    def __init__(self, event: T, view: Optional["ABCView"] = None):
        self.event = event
        self.view = view

        self.handle_responses = []
        self.handlers = []

        self.error: Optional[Exception] = None

        self.pre = self.catch_all(self.pre)  # type: ignore
        self.post = self.catch_all(self.post)  # type: ignore

    def get_handle_response(self, handler) -> Optional[Any]:
        """Get handle response value for handler"""
        for handler_, response in zip(self.handlers, self.handle_responses):
            if handler_ == handler:
                return response

    @property
    def can_forward(self) -> bool:
        """Check if the event can be further processed"""
        return not self.error

    def catch_all(self, func):
        """Catch any exception and save error value"""

        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                self.error = e

        return wrapper

    def stop(self, description: Any = "") -> NoReturn:
        """Wrapper for exception raise"""
        if issubclass(type(description), (Exception,)):
            raise description
        raise MiddlewareError(description)

    async def pre(self) -> None:
        ...

    async def post(self) -> None:
        ...
