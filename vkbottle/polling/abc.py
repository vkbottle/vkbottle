from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Optional

from vkbottle.api import ABCAPI
from vkbottle.exception_factory import ABCErrorHandler


class ABCPolling(ABC):
    """ Abstract Polling class
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/low-level/polling/polling.md
    """

    @abstractmethod
    async def get_server(self) -> Any:
        pass

    @abstractmethod
    async def get_event(self, server: Any) -> dict:
        pass

    @abstractmethod
    async def listen(self) -> AsyncIterator[dict]:
        pass

    @property
    @abstractmethod
    def api(self) -> "ABCAPI":
        pass

    @api.setter
    def api(self, new_api: "ABCAPI"):
        pass

    @abstractmethod
    def construct(
        self, api: "ABCAPI", error_handler: Optional["ABCErrorHandler"] = None
    ) -> "ABCPolling":
        pass
