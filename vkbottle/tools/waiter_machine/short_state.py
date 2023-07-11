import asyncio
import typing

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.handlers.abc import ABCHandler
from vkbottle.dispatch.rules.abc import ABCRule

EventModel = typing.TypeVar("EventModel")
Behaviour = typing.Union[
    typing.Callable[[EventModel], typing.Any],
    ABCHandler[EventModel],
    None,
]


class ShortState(typing.Generic[EventModel]):
    def __init__(
        self,
        ctx_api: ABCAPI,
        event: asyncio.Event,
        rules: typing.Tuple[ABCRule[EventModel], ...],
        default_behaviour: Behaviour = None,
    ) -> None:
        self.ctx_api = ctx_api
        self.event = event
        self.rules = rules
        self.default_behaviour = default_behaviour
