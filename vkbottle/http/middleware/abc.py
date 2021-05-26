import typing
from abc import ABC, abstractmethod

HTTPMiddlewareResponse = typing.NewType("HTTPMiddlewareResponse", bool)


class ABCHTTPMiddleware(ABC):
    """ Abstract class for http-client middleware
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/low-level/http/http-middleware.md
    """

    @abstractmethod
    async def pre(
        self, method: str, url: str, data: typing.Optional[dict] = None, **kwargs
    ) -> typing.Optional[HTTPMiddlewareResponse]:
        pass

    @abstractmethod
    async def post(self, response: typing.Any):
        pass
