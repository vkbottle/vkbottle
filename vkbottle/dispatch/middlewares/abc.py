from abc import ABC
from typing import TYPE_CHECKING, Any, Generic, List, NoReturn, Optional, TypeVar

if TYPE_CHECKING:
    from vkbottle.dispatch.handlers.abc import ABCHandler
    from vkbottle.dispatch.views.abc import ABCView


T = TypeVar("T")


class MiddlewareError(Exception):
    pass


class BaseMiddleware(ABC, Generic[T]):
    event: T
    view: Optional["ABCView"]
    handle_responses: List
    handlers: List["ABCHandler"]

    def __init__(self, event: T, view: Optional["ABCView"] = None):
        self.event = event
        self.view = view

        self.handle_responses = []
        self.handlers = []

        self._new_context: dict = {}
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

    @property
    def context_update(self) -> dict:
        return self._new_context

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

    def send(self, context_update: Optional[dict] = None) -> None:
        """Validate new contxet update data if needed"""
        if context_update is not None:
            if not isinstance(context_update, dict):
                raise ValueError("Context update value should be an instance of dict")
            self._new_context.update(context_update)

    async def pre(self) -> None:
        ...

    async def post(self) -> None:
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
