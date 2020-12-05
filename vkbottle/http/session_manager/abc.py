import typing
from abc import ABC, abstractmethod

from vkbottle.http.client import ABCHTTPClient

HttpClient = typing.Type[ABCHTTPClient]


class ABCSessionManager(ABC):
    _http_client: HttpClient

    @property
    def http_client(self) -> HttpClient:
        return self._http_client

    @http_client.setter
    def http_client(self, http_client: HttpClient):
        self._http_client = http_client

    @abstractmethod
    async def __aenter__(self) -> ABCHTTPClient:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
