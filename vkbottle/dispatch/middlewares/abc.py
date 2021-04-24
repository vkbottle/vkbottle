from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Hashable, List, NewType, NoReturn, Optional

if TYPE_CHECKING:
    from vkbottle.dispatch.handlers.abc import ABCHandler
    from vkbottle.dispatch.views.abc import ABCView
    from vkbottle.tools.dev_tools.mini_types import MessageMin


MiddlewareError = NewType("MiddlewareError", Exception)


class BaseMiddleware(ABC):
    def __init__(self, event: "MessageMin"):
        self.event = event
        self._new_context = {}
        self._error = None

        self.send = self.catch_all(self.send)
        self.error = self.catch_all(self.error)

    @property
    def can_forward(self) -> bool:
        """Check if the event can be further processed"""
        return not self._error

    @property
    def context_update(self) -> dict:
        return self._new_context

    def catch_all(self, func):
        """Catch any exception and save error value"""

        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                self._error = e

        return wrapper

    def error(self, description: Any) -> NoReturn:
        """Wrapper for exception raise"""
        raise MiddlewareError(description)

    def send(self, context_update: Optional[dict] = None) -> None:
        """Validate new contxet update data if needed"""
        if context_update is not None:
            if not isinstance(context_update, dict):
                raise ValueError("Context update value should be an instance of dict")
            self._new_context.update(context_update)

    @abstractmethod
    async def pre(self) -> None:
        ...

    @abstractmethod
    async def post(
        self, view: "ABCView", handle_responses: List[Any], handlers: List["ABCHandler"]
    ):
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
