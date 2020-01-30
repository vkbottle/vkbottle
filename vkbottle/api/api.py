import time
import asyncio
import typing

from termcolor import cprint

from ..const import API_VERSION, API_URL
from .exceptions import VKError
from ..http import HTTPRequest
from ..utils import ContextInstanceMixin


def exception_handler(loop, context):
    pass


async def request(
        token: str,
        method: str,
        params: dict = None,
        session: HTTPRequest = None
):
    url = "{}{method}/?access_token={token}&v={version}".format(
        API_URL,
        method=method,
        token=token,
        version=API_VERSION,
    )

    session = session or HTTPRequest()
    return await session.post(url, data=params or {})


async def request_instance(method: str, req: typing.Coroutine):
    response = await req

    if not isinstance(response, dict):
        while not isinstance(response, dict):
            delay = 1
            cprint(f"\n--- {time.strftime('%m-%d %H:%M:%S')}"
                   f"{time.localtime()} - DELAY {delay * 5} sec\n"
                   f"Check your internet connection. Maybe VK died, request returned: {response}"
                   f"Error appeared after request: {method}",
                   color="yellow",
                   )
            await asyncio.sleep(delay * 5)
            delay += 1
            response = await req

            cprint(f"--- {time.strftime('%m-%d %H:%M:%S', time.localtime())}\n"
                   f"- METHOD SUCCESS after {5 * sum(range(1, delay))} sec\n"
                   f"RESPONSE: {response}\n",
                   color="green"
                   )

    if "error" in response:
        raise VKError(
            [response["error"]["error_code"], response["error"]["error_msg"]]
        )

    return response["response"]


class Method:
    def __init__(self, token: str, method: str):
        self._token = token
        self._method = method

    def __getattr__(self, method):
        if "_" in method:
            m = method.split("_")
            method = m[0] + "".join(i.title() for i in m[1:])

        self._method += "." + method

        return Method(self._token, self._method)

    async def __call__(self, *abandoned, **kwargs):
        if abandoned:
            raise ValueError('Send args with KWARGS! bot.api.a.b(a="b")')

        for k, v in enumerate(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[str(k)] = ",".join(str(x) for x in v)

        req = request(self._token, self._method, kwargs)
        return await request_instance(self._method, req)


class ApiInstance(ContextInstanceMixin):
    def __init__(self, token: str):
        self._token = token
        self._request = HTTPRequest()

    async def request(self, method: str, params: dict):
        req = request(self._token, method, params)
        return await request_instance(method, req)

    def __getattr__(self, method):
        """
        Manage api requests like:
        >>> bot.api.users.get()
        :param method: ignore it
        :return:
        """
        if "_" in method:
            m = method.split("_")
            method = m[0] + "".join(i.title() for i in m[1:])

        return Method(self._token, method)


class UserApi(ApiInstance, ContextInstanceMixin):
    pass


class Api(ApiInstance, ContextInstanceMixin):
    pass
