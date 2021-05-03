from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Hashable, List, NewType, NoReturn, Optional

if TYPE_CHECKING:
    from vkbottle.dispatch.handlers.abc import ABCHandler
    from vkbottle.dispatch.views.abc import ABCView
    from vkbottle.tools.dev_tools.mini_types.bot import MessageMin


class MiddlewareError(Exception):
    pass


class BaseMiddleware(ABC):
    def __init__(self, event: "MessageMin"):
        self.event = event
        self._new_context: dict = {}
        self.error: Optional[Exception] = None

        self.pre = self.catch_all(self.pre)  # type: ignore
        self.post = self.catch_all(self.post)  # type: ignore

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

    def stop(self, description: Any) -> NoReturn:
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

    async def post(
        self, view: "ABCView", handle_responses: List[Any], handlers: List["ABCHandler"]
    ):
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
