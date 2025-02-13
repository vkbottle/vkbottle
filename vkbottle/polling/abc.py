from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any, Optional

from typing_extensions import Self

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class ABCPolling(ABC):
    """Abstract Polling class
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/polling
    """

    @abstractmethod
    async def get_server(self) -> Any:
        pass

    @abstractmethod
    async def get_event(self, server: Any) -> dict:
        pass

    @abstractmethod
    async def listen(self) -> AsyncIterator[dict]:
        yield {}

    @property
    @abstractmethod
    def api(self) -> "ABCAPI":
        pass

    @api.setter  # noqa: B027
    def api(self, new_api: "ABCAPI") -> None:
        pass

    @abstractmethod
    def construct(
        self,
        api: "ABCAPI",
        error_handler: Optional["ABCErrorHandler"] = None,
    ) -> Self:
        pass


__all__ = ("ABCPolling",)
