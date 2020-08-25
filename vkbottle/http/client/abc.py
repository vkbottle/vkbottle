import typing
from abc import ABC, abstractmethod

from vkbottle.http.middleware.abc import request_session_close, ABCHTTPMiddleware
from vkbottle.http.middleware.justlog import JustLogHTTPMiddleware


class ABCHTTPClient(ABC):
    """ Abstract class for http-clients
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/http/http-client.md
    """

    middleware: "ABCHTTPMiddleware" = JustLogHTTPMiddleware()

    @request_session_close
    @abstractmethod
    async def request_text(
        self, method: str, url: str, data: typing.Optional[dict] = None, **kwargs
    ) -> str:
        pass

    @request_session_close
    @abstractmethod
    async def request_json(
        self, method: str, url: str, data: typing.Optional[dict] = None, **kwargs
    ) -> dict:
        pass

    @request_session_close
    @abstractmethod
    async def request_content(
        self, method: str, url: str, data: typing.Optional[dict] = None, **kwargs
    ) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> typing.NoReturn:
        pass
