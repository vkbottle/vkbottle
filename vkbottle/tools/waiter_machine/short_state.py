import asyncio
import dataclasses
import datetime

import typing_extensions as typing

from vkbottle.api.abc import ABCAPI
from vkbottle.dispatch.handlers.abc import ABCHandler
from vkbottle.dispatch.rules.abc import ABCRule

if typing.TYPE_CHECKING:
    from .machine import Identificator

Event = typing.TypeVar("Event")
Behaviour = typing.Union[ABCHandler[Event], None]


class _ShortStateContext(typing.Generic[Event], typing.NamedTuple):
    event: Event
    context: typing.Dict[str, typing.Any]


if typing.TYPE_CHECKING:
    ShortStateContext = _ShortStateContext[Event]

else:
    ShortStateContext = typing.Annotated[_ShortStateContext[Event], ...]


@dataclasses.dataclass
class ShortState(typing.Generic[Event]):
    key: "Identificator"
    ctx_api: ABCAPI
    event: asyncio.Event
    rules: typing.Tuple[ABCRule[Event], ...]
    expiration: dataclasses.InitVar[typing.Optional[datetime.timedelta]] = dataclasses.field(
        default=None,
    )
    default_behaviour: typing.Optional[Behaviour[Event]] = dataclasses.field(default=None)
    on_drop_behaviour: typing.Optional[Behaviour[Event]] = dataclasses.field(default=None)
    exit_behaviour: typing.Optional[Behaviour[Event]] = dataclasses.field(default=None)
    expiration_date: typing.Optional[datetime.datetime] = dataclasses.field(init=False)
    context: typing.Optional[ShortStateContext[Event]] = dataclasses.field(
        default=None,
        init=False,
    )

    def __post_init__(self, expiration: typing.Optional[datetime.timedelta]) -> None:
        self.creation_date = datetime.datetime.now()
        self.expiration_date = (
            (self.creation_date + expiration) if expiration is not None else None
        )

    def cancel(self) -> None:
        """Cancel schedule waiters."""

        waiters = typing.cast(
            "typing.Iterable[asyncio.Future[typing.Any]]",
            self.event._waiters,  # type: ignore
        )
        for future in waiters:
            future.cancel()


__all__ = ("ShortState",)
