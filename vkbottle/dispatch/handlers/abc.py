from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Union, Optional, overload

if TYPE_CHECKING:
    from vkbottle_types.events import Event


class ABCHandler(ABC):
    blocking: bool

    @overload
    @abstractmethod
    async def filter(self, event: "Event") -> Union[dict, bool]:
        pass

    @overload
    @abstractmethod
    async def filter(
        self,
        event: "Event",
        context_variables: Optional[dict] = None
    ) -> Union[dict, bool]:
        pass

    @abstractmethod
    async def handle(self, event: "Event", **context) -> Any:
        pass
