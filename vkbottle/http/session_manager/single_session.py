from typing import TYPE_CHECKING, Optional, Type

from vkbottle.http.client import AiohttpClient

from .abc import ABCSessionManager

if TYPE_CHECKING:
    from vkbottle.http.client import ABCHTTPClient


class SingleSessionManager(ABCSessionManager):
    def __init__(self, http_client: Optional[Type["ABCHTTPClient"]] = None, **kwargs):
        super().__init__()
        self.http_client: Type["ABCHTTPClient"] = http_client or AiohttpClient
        self.http_client_settings = kwargs
        self._session: Optional["ABCHTTPClient"] = None

    @property
    def session(self) -> "ABCHTTPClient":
        if not self._session:
            self._session = self.http_client(**self.http_client_settings)
        return self._session

    async def __aenter__(self) -> "ABCHTTPClient":
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
