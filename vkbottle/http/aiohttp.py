import asyncio
from typing import TYPE_CHECKING, Any, Optional

from aiohttp import ClientSession, TCPConnector

from vkbottle.modules import json as json_module

from .abc import ABCHTTPClient

if TYPE_CHECKING:
    from vkbottle.http.middleware.abc import ABCHTTPMiddleware


class AiohttpClient(ABCHTTPClient):
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        session: Optional[ClientSession] = None,
        middleware: Optional["ABCHTTPMiddleware"] = None,
        json_processing_module: Optional[Any] = None,
        optimize: bool = False,
        **kwargs,
    ):
        self.loop = loop or asyncio.get_event_loop()
        self.json_processing_module = json_processing_module or json_module

        if optimize:
            kwargs["skip_auto_headers"] = {"User-Agent"}
            kwargs["raise_for_status"] = True

        self.session = session or ClientSession(
            connector=TCPConnector(ssl=False),
            json_serialize=self.json_processing_module.dumps,
            **kwargs,
        )

        if middleware is not None:
            self.middleware = middleware

    async def request_json(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> dict:
        async with self.session.request(method, url, data=data, **kwargs) as response:
            return await response.json(loads=self.json_processing_module.loads)

    async def request_text(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> str:
        async with self.session.request(method, url, data=data, **kwargs) as response:
            return await response.text()

    async def request_content(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> bytes:
        async with self.session.request(method, url, data=data, **kwargs) as response:
            return await response.content.read()

    async def close(self) -> None:
        await self.session.close()
