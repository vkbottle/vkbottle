"""Read LICENSE.txt"""

"""
VKBOTTLE WORK TOOLS
"""

from collections import MutableMapping
from aiohttp import ClientSession
from ..portable import VERSION_PORTABLE
from ..jsontype import json
import ssl


def dict_of_dicts_merge(d1, d2):
    """
    Update two dicts of dicts recursively,
    if either mapping has leaves that are non-dicts,
    the second's leaf overwrites the first's.
    """
    for k, v in d1.items():
        if k in d2:
            if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                d2[k] = dict_of_dicts_merge(v, d2[k])
    d3 = d1.copy()
    d3.update(d2)
    return d3


def make_priority_path(first: dict, priority, compile, second):
    """
    Make priority path for processors of Events class,
    [deprecated] [deprecated] [deprecated]
    fixme RU - убрать это нечто и перевести в мердж приоритетов
    """
    if priority not in first:
        first[priority] = {}
    if compile is not None:
        first[priority][compile] = second
    else:
        first[priority] = second
    return first


async def sorted_dict_keys(dictionary: dict, reverse=True):
    return sorted(list(dictionary.keys()), reverse=reverse)


def _request(func):
    """
    aioHTTP Request Decorator Wrapper
    :param func: wrapped function
    """
    async def decorator(*args, **kwargs):
        async with ClientSession(json_serialize=json.dumps) as client:
            funced = await func(*args, **kwargs, client=client)
        return funced
    return decorator


class HTTPRequest(object):
    """
    aioHTTP Request Wrapper
    """
    def __init__(self):
        self.client = ClientSession(json_serialize=json.dumps)

    @_request
    async def post(self, url, params: dict = None, client: ClientSession = None, content_type='application/json'):
        params = params or {}
        async with client.post(url, params=params, ssl=ssl.SSLContext()) as response:
            return await response.json(content_type=content_type)

    @_request
    async def get(self, url, client: ClientSession = None, content_type='application/json'):
        async with client.get(url, ssl=ssl.SSLContext()) as response:
            return await response.json(content_type=content_type)


class HTTP(object):
    request = HTTPRequest()

    async def get_current_portable(self):
        """
        Get current actual info about package from GitHub page
        todo RU - перевести мониторинг на свой домен
        """
        portable = await self.request.get(url=VERSION_PORTABLE, content_type='text/plain')
        return portable


class ErrorHandler(object):
    def __init__(self):
        self._error_processors = dict()

    def __call__(self, *error_numbers):
        def decorator(func):
            for error_number in error_numbers:
                self._error_processors[error_number] = {'call': func}
            return func
        return decorator

    def get_processor(self):
        return self._error_processors

