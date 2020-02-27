import time
import asyncio

from ..utils import logger

from ..const import API_VERSION, API_URL
from .exceptions import VKError
from ..http import HTTPRequest
from ..utils import ContextInstanceMixin
from .token import TokenQueue


def exception_handler(loop, context):
    pass


class NonTokenQueue:
    def __init__(self, token: str):
        self.token = token

    def __call__(self):
        return self

    def get(self):
        return self.token


async def request(
    token: str, method: str, params: dict = None, session: HTTPRequest = None
):
    url = "{}{method}/?access_token={token}&v={version}".format(
        API_URL, method=method, token=token, version=API_VERSION,
    )

    session = session or HTTPRequest()
    return await session.post(url, data=params or {})


async def request_instance(method: str, req: tuple):
    response = await request(*req)

    if not isinstance(response, dict):
        while not isinstance(response, dict):
            # Works only on python 3.6+
            delay = 1
            logger.critical(
                "\n---"
                f"{time.localtime()} - DELAY {delay * 5} sec\n"
                f"Check your internet connection. Maybe VK died, request returned: {response}"
                f"Error appeared after request: {method}",
            )
            await asyncio.sleep(delay * 5)
            delay += 1
            response = await request(*req)

            logger.critical(
                f"--- {time.strftime('%m-%d %H:%M:%S', time.localtime())}\n"
                f"- METHOD SUCCESS after {5 * sum(range(1, delay))} sec\n"
                f"RESPONSE: {response}\n",
            )

    if "error" in response:
        logger.debug(
            "Error after request {method}, response: {r}", method=method, r=response
        )
        raise VKError([response["error"]["error_code"], response["error"]["error_msg"]])

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

        for k, v in kwargs.items():
            if isinstance(v, (list, tuple)):
                kwargs[k] = ",".join(str(x) for x in v)

        return await request_instance(self._method, (self._token, self._method, kwargs))


class ApiInstance(ContextInstanceMixin):
    def __init__(self, use_token_queue: bool = False, token: str = None):
        if use_token_queue:
            self._token_queue = TokenQueue.get_current
        else:
            self._token_queue = NonTokenQueue(token)
        self._request = HTTPRequest()

    @property
    def token(self):
        return self._token_queue().get()

    async def request(self, method: str, params: dict):
        return await request_instance(method, (self.token, method, params))

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

        return Method(self.token, method)


class UserApi(ApiInstance, ContextInstanceMixin):
    pass


class Api(ApiInstance, ContextInstanceMixin):
    pass
