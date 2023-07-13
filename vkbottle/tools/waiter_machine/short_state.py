import asyncio
import datetime
import typing

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.rules.abc import ABCRule

if typing.TYPE_CHECKING:
    from .machine import Identificator

EventModel = typing.TypeVar("EventModel")
Behaviour = typing.Union[
    typing.Callable[
        [typing.Optional[EventModel]],
        typing.Union[typing.Coroutine[typing.Any, None, None], typing.Any],
    ],
    None,
]


class ShortState(typing.Generic[EventModel]):
    def __init__(
        self,
        key: "Identificator",
        ctx_api: ABCAPI,
        event: asyncio.Event,
        rules: typing.Tuple[ABCRule[EventModel], ...],
        expiration: typing.Optional[datetime.timedelta] = None,
        default_behaviour: Behaviour = None,
        on_drop_behaviour: Behaviour = None,
    ) -> None:
        self.key = key
        self.ctx_api = ctx_api
        self.event = event
        self.rules = rules
        self.default_behaviour = default_behaviour
        self.expiration = (datetime.datetime.now() + expiration) if expiration else None
        self.on_drop_behaviour = on_drop_behaviour
