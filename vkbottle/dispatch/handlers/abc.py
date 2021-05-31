from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from vkbottle_types.events import Event


class ABCHandler(ABC):
    blocking: bool

    @abstractmethod
    async def filter(self, event: "Event") -> Union[dict, bool]:
        pass

    @abstractmethod
    async def handle(self, event: "Event", **context) -> Any:
        pass
