from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

from aiohttp import ClientSession

from vkbottle.modules import json as json_module
from vkbottle.modules import logger

from .abc import ABCHTTPClient

if TYPE_CHECKING:
    from aiohttp import ClientResponse

TSingleAiohttpClient = TypeVar("TSingleAiohttpClient", bound="SingleAiohttpClient")


class AiohttpClient(ABCHTTPClient):
    def __init__(
        self,
        session: Optional[ClientSession] = None,
        json_processing_module: Optional[Any] = None,
        optimize: bool = False,
        **session_params,
    ):
        self.json_processing_module = (
            json_processing_module or session_params.pop("json_serialize", None) or json_module
        )

        if optimize:
            session_params["skip_auto_headers"] = {"User-Agent"}
            session_params["raise_for_status"] = True
        if session_params.pop("loop", None):
            logger.warning("loop argument is deprecated")

        self.session = session

        self._session_params = session_params

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs,
    ) -> "ClientResponse":
        if not self.session:
            self.session = ClientSession(
                json_serialize=self.json_processing_module.dumps,
                **self._session_params,
            )
        async with self.session.request(url=url, method=method, data=data, **kwargs) as response:
            await response.read()
            return response

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding="utf-8", loads=self.json_processing_module.loads, content_type=None
        )

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs,
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text(encoding="utf-8")

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return response._body

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def __del__(self):
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector.close()
            self.session._connector = None


class SingleAiohttpClient(AiohttpClient):
    __instance__ = None

    def __new__(
        cls: Type[TSingleAiohttpClient], *args: Any, **kwargs: Any
    ) -> TSingleAiohttpClient:
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls, *args, **kwargs)
        return cls.__instance__

    def __aexit__(self, exc_type, exc_val, exc_tb):
        pass  # no need to close session in this case
