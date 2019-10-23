from ..const import API_VERSION, API_URL
from .exceptions import VKError
from ..http import HTTPRequest
from asyncio import AbstractEventLoop, get_event_loop


class Method(object):
    """
    VK API Method

    Universal for User and Bot API. Make single async requests to VK API Server
    """

    def __init__(
        self, token: str, loop: AbstractEventLoop = None, request: HTTPRequest = None
    ):
        """
        :param token: VK API Token (universal for User and Bot API)
        :param request: aioHTTP ClientSession for ordered sessions
        """
        self.loop = loop
        self._token = token
        self.request = request or HTTPRequest()

    def generate_method_url(self, group, method, execute: bool = False):
        return (
            API_URL
            + "{group}.{method}/?access_token={token}&v={version}".format(
                group=group, method=method, token=self._token, version=API_VERSION
            )
            if not execute
            else API_URL
            + "execute/?access_token={token}&v={version}".format(
                group=group, method=method, token=self._token, version=API_VERSION
            )
        )

    async def __call__(
        self, group: str, method: str, params: dict = None, _execute: bool = False
    ):
        """
        VK API Method Wrapper
        :param group: method group
        :param method: method name
        :return: VK API Server Response
        """

        response = await self.request.post(
            url=self.generate_method_url(group, method, _execute), params=params
        )

        if "error" in response:
            raise VKError(
                [response["error"]["error_code"], response["error"]["error_msg"]]
            )
        return response["response"]


class Api(object):
    """
    Allow to make requests like this:
    >>> bot.api.messages.send(**kwargs)
    FIXME: This thing should be fixed

    Receive only kwargs, no positional arguments. Kwargs can be skipped
    """

    def __init__(self, loop: AbstractEventLoop, token: str, group_id: int, method=None):
        """
        VK Api Wrapper
        :param loop: asyncio event loop
        :param group_id:
        :param method:
        """

        self.loop: AbstractEventLoop = loop or get_event_loop()
        self._token: str = token
        self.method_object: Method = Method(token, self.loop)
        self.group_id: int = group_id
        self._method = method

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

        return Api(
            self.loop,
            self._token,
            self.group_id,
            (self._method + "." if self._method else "") + method,
        )

    async def request(self, group, method, data: dict = None) -> dict:
        data = {k: v for k, v in data.items() if v is not None} if data else {}
        return await self.method_object(group, method, data)

    async def execute(self, code: str) -> dict:
        data = {"code": code}
        return await self.method_object("", "", data, _execute=True)

    async def __call__(self, **kwargs) -> dict:
        """
        API Method Maker
        :param kwargs: all data of the request
        :return: VK Server Response
        """

        for k, v in enumerate(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ",".join(str(x) for x in v)

        method = self._method.split(".")

        if len(method) == 2:
            group = method[0]
            method = method[1]

            return await self.method_object(group, method, kwargs)
