from __future__ import annotations

import asyncio
import atexit
import warnings
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from typing import TYPE_CHECKING, Any

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
        session: ClientSession | None = None,
        json_processing_module: JSONModule | None = None,
        optimize: bool = False,
        **session_params: Unpack[AiohttpSessionKwargs],
    ) -> None:
        json_serialize = session_params.pop("json_serialize", None)
        self.json_processing_module = json_processing_module or json_serialize or json_module

        if optimize:
            session_params["skip_auto_headers"] = {"User-Agent"}
            session_params["raise_for_status"] = True

        self.session = session
        # Loop the auto-created session is bound to; None when the caller supplied
        # the session (its lifecycle is then the caller's responsibility).
        self._session_loop: asyncio.AbstractEventLoop | None = None
        self._session_params = session_params

        atexit.register(self.close_connector)

    @asynccontextmanager
    async def request(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> AsyncGenerator[ClientResponse]:
        if (
            self.session is None
            or self.session.closed
            or (
                self._session_loop is not None
                and self._session_loop is not asyncio.get_running_loop()
            )
        ):
            self.session = ClientSession(  # type: ignore[misc]
                json_serialize=self._json_serialize,
                **self._session_params,  # type: ignore[arg-type]
            )
            self._session_loop = asyncio.get_running_loop()

        async with self.session.request(url=url, method=method, data=data, **kwargs) as response:
            yield response

    async def request_raw(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> ClientResponse:
        async with self.request(url, method, data, **kwargs) as response:
            await response.read()
            return response

    async def request_json(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
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
        data: dict[str, Any] | None = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> str:
        async with self.request(url, method, data, **kwargs) as response:
            return await response.text(encoding="UTF-8")

    async def request_content(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Unpack[AiohttpRequestKwargs],
    ) -> bytes:
        async with self.request(url, method, data, **kwargs) as response:
            return await response.read()

    def _json_serialize(self, obj: Any) -> str:
        # aiohttp's json_serialize must return str, but some json modules (orjson)
        # return bytes from dumps(); normalise to str.
        result = self.json_processing_module.dumps(obj)
        return result.decode() if isinstance(result, bytes) else result

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
            with warnings.catch_warnings(), suppress(Exception):
                warnings.simplefilter(action="ignore", category=RuntimeWarning)
                self.session.connector.close().__await__().send(None)
            self.session.detach()


class SingleAiohttpClient(AiohttpClient, ABCSingleton):
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        pass  # no need to close session in this case
