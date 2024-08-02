from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from types import TracebackType


class ABCHTTPClient(ABC):
    """Abstract class for http-clients
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/http-client
    """

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Any,
    ) -> Any:
        pass

    @abstractmethod
    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Any,
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Any,
    ) -> dict:
        pass

    @abstractmethod
    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> "ABCHTTPClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional["TracebackType"],
    ) -> None:
        await self.close()
