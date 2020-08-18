import ssl
import traceback
import typing

from aiohttp import ClientSession

from vkbottle.const import VERSION_REST, __version__
from vkbottle.utils import json, logger
from .proxy import Proxy


def request_decorator(func):
    """
    aioHTTP Request Decorator Wrapper
    :param func: wrapped function
    """

    async def decorator(*args, **kwargs):
        try:
            async with ClientSession(json_serialize=json.dumps) as client:
                response = await func(*args, **kwargs, client=client)
            return response
        except Exception as e:
            logger.error(f"Error while requesting:\n{traceback.format_exc()}")

    return decorator


class HTTPRequest:
    """
    aioHTTP Request Wrapper
    """

    def __init__(self):
        pass

    @request_decorator
    async def post(
        self,
        url: str,
        params: dict = None,
        client: ClientSession = None,
        data: dict = None,
        json_: dict = None,
        content_type: str = "application/json",
        read_content: bool = False,
    ) -> typing.Union[dict]:
        async with client.post(
            url,
            params=params or {},
            ssl=ssl.SSLContext(),
            data=data,
            json=json_,
            **self.proxy_params,
        ) as response:
            if read_content:
                return await response.content.read()
            return await response.json(content_type=content_type)

    @request_decorator
    async def get(
        self,
        url: str,
        client: ClientSession = None,
        data: dict = None,
        json_: dict = None,
        content_type: str = "application/json",
        read_content: bool = False,
    ) -> typing.Union[dict, bytes]:
        async with client.get(
            url,
            ssl=ssl.SSLContext(),
            data=data or None,
            json=json_ or None,
            **self.proxy_params,
        ) as response:
            if read_content:
                return await response.content.read()
            return await response.json(content_type=content_type)

    @property
    def proxy_params(self) -> dict:
        if self.proxy:
            return {
                "proxy": self.proxy.get_proxy(),
                "proxy_auth": self.proxy.get_auth(),
            }
        return {}

    @property
    def proxy(self) -> Proxy:
        return Proxy.get_current()

    def __repr__(self):
        return "<HTTPRequest>"


class HTTP:
    request = HTTPRequest()

    async def get_current_rest(self) -> dict:
        """
        Get current actual info about package from GitHub REST page
        """
        rest_status = await self.request.get(
            url=VERSION_REST, content_type="text/plain"
        )
        if rest_status is None:
            logger.info("Unable to check version! Skipping it")
            return {"version": __version__}
        return rest_status

    def __repr__(self):
        return "<HTTP>"
