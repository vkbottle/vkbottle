from aiohttp import ClientSession
import json
import ssl
from asyncio import Future


def request(func):
    """
    aioHTTP Request Decorator Wrapper
    :param func: wrapped function
    """
    async def decorator(*args, **kwargs):
        async with ClientSession(json_serialize=json.dumps) as client:
            response = await func(*args, **kwargs, client=client)
        return response
    return decorator


class HTTPRequest(object):
    """
    aioHTTP Request Wrapper
    """
    def __init__(self):
        pass

    @request
    async def post(self,
                   url: str,
                   params: dict = None,
                   client: ClientSession = None,
                   data: dict = None,
                   json: dict = None,
                   content_type: str = 'application/json'
                   ):
        async with client.post(url,
                               params=params or {},
                               ssl=ssl.SSLContext(),
                               data=data or None,
                               json=json or None) as response:
            return await response.json(content_type=content_type)

    @request
    async def get(self,
                  url: str,
                  client: ClientSession = None,
                  data: dict = None,
                  json: dict = None,
                  content_type: str = 'application/json'
                  ):
        async with client.get(url,
                              ssl=ssl.SSLContext(),
                              data=data or None,
                              json=json or None) as response:
            return await response.json(content_type=content_type)


class HTTP(object):
    request = HTTPRequest()
