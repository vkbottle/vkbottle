import ssl
import traceback

from aiohttp import ClientSession

from vkbottle.const import VERSION_REST, __version__
from vkbottle.utils import json, logger


def request(func):
    """
    aioHTTP Request Decorator Wrapper
    :param func: wrapped function
    """

    async def decorator(*args, **kwargs):
        try:
            async with ClientSession(json_serialize=json.dumps) as client:
                response = await func(*args, **kwargs, client=client)
            return response
        except Exception:
            logger.error(f"Error while requesting:\n{traceback.format_exc()}")

    return decorator


class HTTPRequest:
    """
    aioHTTP Request Wrapper
    """

    def __init__(self):
        pass

    @request
    async def post(
        self,
        url: str,
        params: dict = None,
        client: ClientSession = None,
        data: dict = None,
        json_: dict = None,
        content_type: str = "application/json",
    ) -> dict:
        async with client.post(
            url, params=params or {}, ssl=ssl.SSLContext(), data=data, json=json_,
        ) as response:
            return await response.json(content_type=content_type)

    @request
    async def get(
        self,
        url: str,
        client: ClientSession = None,
        data: dict = None,
        json_: dict = None,
        content_type: str = "application/json",
    ) -> dict:
        async with client.get(
            url, ssl=ssl.SSLContext(), data=data or None, json=json_ or None
        ) as response:
            return await response.json(content_type=content_type)

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
