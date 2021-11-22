import asyncio
import dataclasses
import typing

from vkbottle.dispatch.rules.abc import ABCRule

DefaultWaiterHandler = typing.Callable[..., typing.Coroutine]

T = typing.TypeVar("T")


@dataclasses.dataclass
class Waiter:
    rules: typing.List[ABCRule]
    event: asyncio.Event
    default: typing.Optional[typing.Union[DefaultWaiterHandler, typing.Any]] = None


class Await(typing.Generic[T]):
    def __init__(self, waiter: Waiter):
        self.waiter = waiter

    async def __aenter__(self) -> T:
        await self.waiter.event.wait()
        return getattr(self.waiter.event, "e")  # noqa

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
