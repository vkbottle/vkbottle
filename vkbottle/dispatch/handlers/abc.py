from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Union, overload

from typing_extensions import Protocol

if TYPE_CHECKING:
    from vkbottle_types.events import Event


class CleanFilter(Protocol):
    async def __call__(self, event: "Event") -> Union[dict, bool]:
        pass


class ContextFilter(Protocol):
    async def __call__(
        self, event: "Event", context_variables: Optional[dict] = None
    ) -> Union[dict, bool]:
        pass


class ABCHandler(ABC):
    blocking: bool

    @property
    @abstractmethod
    def filter(self) -> Union[CleanFilter, ContextFilter]:
        pass

    @abstractmethod
    async def handle(self, event: "Event", **context) -> Any:
        pass
