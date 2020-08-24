import asyncio
import typing
from ssl import SSLContext

from aiohttp import ClientSession, TCPConnector

from vkbottle.modules import json as json_module
from .abc import ABCHTTPClient


class AiohttpClient(ABCHTTPClient):
    def __init__(
        self,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        session: typing.Optional[ClientSession] = None
    ):
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or ClientSession(
            connector=TCPConnector(verify_ssl=False, ssl_context=SSLContext(), loop=self.loop,),
            json_serialize=json_module.dumps,
        )

    async def request_json(
        self,
        method: str,
        url: str,
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> dict:
        async with self.session.request(method, url, data=data, **kwargs) as response:
            return await response.json(loads=json_module.loads)

    async def request_text(
        self,
        method: str,
        url: str,
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> str:
        async with self.session.request(method, url, data=data, **kwargs) as response:
            return await response.text()

    async def request_content(
        self,
        method: str,
        url: str,
        data: typing.Optional[dict] = None,
        **kwargs
    ) -> bytes:
        async with self.session.request(method, url, data=data, **kwargs) as response:
            return await response.content.read()
