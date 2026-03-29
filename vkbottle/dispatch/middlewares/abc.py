from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, NoReturn, TypeVar

if TYPE_CHECKING:
    from vkbottle.dispatch.handlers.abc import ABCHandler
    from vkbottle.dispatch.views.abc import ABCView


T = TypeVar("T")


class MiddlewareError(Exception):
    pass


class ABCMiddleware(ABC):
    @abstractmethod
    def stop(self, error: Any) -> NoReturn: ...

    @abstractmethod
    def send(self, context_update: dict[str, Any] | None = None) -> None: ...

    @abstractmethod
    async def pre(self) -> None: ...

    @abstractmethod
    async def post(self) -> None: ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class BaseMiddleware(Generic[T]):
    event: T
    view: "ABCView | None"
    handle_responses: list[Any]
    handlers: list["ABCHandler"]

    def __init__(self, event: T, view: "ABCView | None" = None):
        self.event = event
        self.view = view

        self.handle_responses = []
        self.handlers = []

        self._new_context: dict[str, Any] = {}
        self.error: Exception | None = None

        self.pre = self.catch_all(self.pre)  # type: ignore
        self.post = self.catch_all(self.post)  # type: ignore

    def get_handle_response(self, handler) -> Any | None:
        """Get handle response value for handler"""
        for handler_, response in zip(self.handlers, self.handle_responses):
            if handler_ == handler:
                return response

    @property
    def can_forward(self) -> bool:
        """Check if the event can be further processed"""

        return not self.error

    @property
    def context_update(self) -> dict[str, Any]:
        return self._new_context

    def catch_all(self, func):
        """Catch any exception and save error value"""

        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                self.error = e

        return wrapper

    def stop(self, error: str | Exception | type[Exception] | None = None) -> NoReturn:
        """Wrapper for exception raise"""

        if error is None or isinstance(error, str):
            raise MiddlewareError(error or "")
        raise error

    def send(self, context_update: dict[str, Any] | None = None) -> None:
        """Validate new context update data if needed"""

        if context_update is not None:
            if not isinstance(context_update, dict):
                msg = "Context update value should be an instance of dict"
                raise ValueError(msg)
            self._new_context.update(context_update)

    async def pre(self) -> None: ...

    async def post(self) -> None: ...


__all__ = ("ABCMiddleware", "BaseMiddleware", "MiddlewareError")
