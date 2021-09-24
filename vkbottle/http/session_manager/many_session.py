from typing import TYPE_CHECKING, Optional, Type

from vkbottle.http.client import AiohttpClient

from .abc import ABCSessionManager

if TYPE_CHECKING:
    from vkbottle.http.client import ABCHTTPClient


class ManySessionManager(ABCSessionManager):
    def __init__(self, http_client: Optional[Type["ABCHTTPClient"]] = None):
        super().__init__()
        self.http_client = http_client or AiohttpClient
        self._active_session: Optional["ABCHTTPClient"] = None

    async def __aenter__(self) -> "ABCHTTPClient":
        self._active_session = self.http_client()
        return self._active_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._active_session.close()
