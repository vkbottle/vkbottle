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
Behaviour = ABCHandler[Event] | None


class _ShortStateContext(typing.Generic[Event], typing.NamedTuple):
    event: Event
    context: dict[str, typing.Any]


if typing.TYPE_CHECKING:
    ShortStateContext = _ShortStateContext[Event]

else:
    ShortStateContext = typing.Annotated[_ShortStateContext[Event], ...]


@dataclasses.dataclass
class ShortState(typing.Generic[Event]):
    key: "Identificator"
    ctx_api: ABCAPI
    event: asyncio.Event
    rules: tuple[ABCRule[Event], ...]
    expiration: dataclasses.InitVar[datetime.timedelta | None] = dataclasses.field(
        default=None,
    )
    default_behaviour: Behaviour[Event] | None = dataclasses.field(default=None)
    on_drop_behaviour: Behaviour[Event] | None = dataclasses.field(default=None)
    exit_behaviour: Behaviour[Event] | None = dataclasses.field(default=None)
    expiration_date: datetime.datetime | None = dataclasses.field(init=False)
    context: ShortStateContext[Event] | None = dataclasses.field(
        default=None,
        init=False,
    )

    def __post_init__(self, expiration: datetime.timedelta | None) -> None:
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
