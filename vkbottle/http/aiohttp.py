import asyncio
from typing import TYPE_CHECKING, Any, Optional

from aiohttp import ClientSession, TCPConnector

from vkbottle.modules import json as json_module
from vkbottle.tools.dev.singleton import Singleton

from .abc import ABCHTTPClient

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class AiohttpClient(ABCHTTPClient):
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        session: Optional[ClientSession] = None,
        json_processing_module: Optional[Any] = None,
        optimize: bool = False,
        **kwargs,
    ):
        self.loop = loop or asyncio.get_event_loop()
        self.json_processing_module = json_processing_module or json_module

        if optimize:
            kwargs["skip_auto_headers"] = {"User-Agent"}
            kwargs["raise_for_status"] = True

        self.session = session

        self.__session_params = kwargs

    async def request_raw(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> "ClientResponse":
        if not self.session:
            self.session = ClientSession(
                connector=TCPConnector(ssl=False),
                json_serialize=self.json_processing_module.dumps,
                **self.__session_params,
            )
        async with self.session.request(url=url, method=method, data=data, **kwargs) as response:
            await response.read()
            return response

    async def request_json(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> dict:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(encoding="utf-8", loads=self.json_processing_module.loads)

    async def request_text(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text(encoding="utf-8")

    async def request_content(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.content.read()

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def __del__(self):
        if self.session and not self.session.closed:
            if self._connector is not None and self._connector_owner:
                self.session._connector.close()
            self._connector = None


class SingleAiohttpClient(AiohttpClient, Singleton):
    def __aexit__(self, exc_type, exc_val, exc_tb):
        pass  # no need to close session in this case
