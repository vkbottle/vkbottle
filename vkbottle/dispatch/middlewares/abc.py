from abc import ABC
from typing import TYPE_CHECKING, Any, List, NewType

if TYPE_CHECKING:
    from vkbottle.dispatch.views.abc import ABCView
    from vkbottle.dispatch.handlers.abc import ABCHandler


MiddlewareResponse = NewType("MiddlewareResponse", bool)


class BaseMiddleware(ABC):
    async def pre(self, event):
        ...

    async def post(
        self, event, view: "ABCView", handle_responses: List[Any], handlers: List["ABCHandler"]
    ):
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
