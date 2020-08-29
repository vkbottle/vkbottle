from .abc import ABCSessionManager
from vkbottle.http.client import ABCHTTPClient, AiohttpClient
import typing


class SessionManager(ABCSessionManager):
    def __init__(self, http_client: typing.Optional[typing.Type[ABCHTTPClient]] = None):
        self.http_client = http_client or AiohttpClient
        self._active_session: typing.Optional[ABCHTTPClient] = None

    async def __aenter__(self) -> ABCHTTPClient:
        self._active_session = self.http_client()
        return self._active_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._active_session.close()
