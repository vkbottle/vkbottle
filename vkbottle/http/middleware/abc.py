from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from vkbottle.http.client.abc import ABCHTTPClient

HTTPMiddlewareResponse = typing.NewType("HTTPMiddlewareResponse", bool)


def http_middleware_decorator(
        func: typing.Callable[[str, str, typing.Optional[dict]], typing.Any]
) -> typing.Callable[["ABCHTTPClient", str, str, typing.Optional[dict]], typing.Any]:
    """ Wrap request method running middlewares """
    async def wrapper(http_client: "ABCHTTPClient", *args, **kwargs) -> typing.Any:
        if await http_client.middleware.pre(*args, **kwargs) == HTTPMiddlewareResponse(False):
            return None

        response = await func(http_client, *args, **kwargs)
        await http_client.middleware.post(response)

        return response
    return wrapper


class ABCHTTPMiddleware(ABC):

    @abstractmethod
    async def pre(
        self,
        method: str,
        url: str,
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> typing.Optional[HTTPMiddlewareResponse]:
        pass

    @abstractmethod
    async def post(self, response: typing.Any):
        pass
