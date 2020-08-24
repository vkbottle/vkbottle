from abc import ABC, abstractmethod
import typing
from vkbottle.http.middleware.abc import http_middleware_decorator, ABCHTTPMiddleware
from vkbottle.http.middleware.justlog import JustLogHTTPMiddleware


class ABCHTTPClient(ABC):

    middleware: "ABCHTTPMiddleware" = JustLogHTTPMiddleware()

    @http_middleware_decorator
    @abstractmethod
    async def request_text(
        self,
        method: str,
        url: str,
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> str:
        pass

    @http_middleware_decorator
    @abstractmethod
    async def request_json(
        self,
        method: str,
        url: str,
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> dict:
        pass

    @http_middleware_decorator
    @abstractmethod
    async def request_content(
        self,
        method: str,
        url: str,
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> bytes:
        pass
