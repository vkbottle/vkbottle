import typing
from abc import ABC, abstractmethod
from typing import Any, Union

Event = typing.TypeVar("Event")


class ABCHandler(ABC, typing.Generic[Event]):
    blocking: bool

    @abstractmethod
    async def filter(self, event: Event) -> Union[dict, bool]:
        pass

    @abstractmethod
    async def handle(self, event: Event, **context) -> Any:
        pass
