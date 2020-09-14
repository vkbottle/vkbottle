from abc import ABC
from typing import Any
from typing import List
from typing import NewType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vkbottle.dispatch.views.abc import ABCView

MiddlewareResponse = NewType("MiddlewareResponse", bool)


class BaseMiddleware(ABC):
    async def pre(self, event):
        ...

    async def post(self, event, view: "ABCView", handle_responses: List[Any]):
        ...
