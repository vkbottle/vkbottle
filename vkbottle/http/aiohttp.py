from __future__ import annotations

import atexit
from contextlib import asynccontextmanager, suppress
from typing import TYPE_CHECKING, Any, AsyncGenerator, Optional, Type

from aiohttp import ClientSession

from vkbottle.modules import json as json_module
from vkbottle.tools.singleton import ABCSingleton

from .abc import ABCHTTPClient

if TYPE_CHECKING:
    from types import TracebackType

    from aiohttp import ClientResponse
    from typing_extensions import Unpack

    from vkbottle.modules import JSONModule

    from .aiohttp_types import AiohttpRequestKwargs, AiohttpSessionKwargs


class AiohttpClient(ABCHTTPClient):
    def __init__(
        self,
        session: Optional[ClientSession] = None,
        json_processing_module: Optional[JSONModule] = None,
        optimize: bool = False,
        **session_params: Unpack[AiohttpSessionKwargs],
    ) -> None:
        json_serialize = session_params.pop("json_serialize", None)
        self.json_processing_module = json_processing_module or json_serialize or json_module

        if optimize:
            session_params["skip_auto_headers"] = {"User-Agent"}
            session_params["raise_for_status"] = True

        self.session = session
        self._session_params = session_params

        atexit.register(self.close_connector)

    @asynccontextmanager
    async def request(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> AsyncGenerator[ClientResponse, None]:
        if not self.session:
            self.session = ClientSession(  # type: ignore[misc]
                json_serialize=self.json_processing_module.dumps,
                **self._session_params,  # type: ignore[arg-type]
            )

        async with self.session.request(url=url, method=method, data=data, **kwargs) as response:
            yield response

    async def request_raw(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> ClientResponse:
        async with self.request(url, method, data, **kwargs) as response:
            await response.read()
            return response

    async def request_json(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> dict[str, Any]:
        async with self.request(url, method, data, **kwargs) as response:
            return await response.json(
                encoding="UTF-8",
                loads=self.json_processing_module.loads,
                content_type=None,
            )

    async def request_text(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> str:
        async with self.request(url, method, data, **kwargs) as response:
            return await response.text(encoding="UTF-8")

    async def request_content(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> bytes:
        async with self.request(url, method, data, **kwargs) as response:
            return await response.read()

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def close_connector(self) -> None:
        if (
            self.session is not None
            and not self.session.closed
            and self.session.connector_owner is True
            and self.session.connector is not None
            and not self.session.connector.closed
        ):
            with suppress(Exception):
                self.session.connector.close().__await__().send(None)
            self.session.detach()


class SingleAiohttpClient(AiohttpClient, ABCSingleton):
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        pass  # no need to close session in this case
