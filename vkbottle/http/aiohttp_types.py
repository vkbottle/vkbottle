from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable, Mapping
from typing import (
    TYPE_CHECKING,
    Any,
)

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from ssl import SSLContext

    from aiohttp import (
        BaseConnector,
        BasicAuth,
        ClientRequest,
        ClientResponse,
        ClientTimeout,
        ClientWebSocketResponse,
        Fingerprint,
        HttpVersion,
        TraceConfig,
    )
    from aiohttp.abc import AbstractCookieJar
    from aiohttp.typedefs import LooseCookies, LooseHeaders, StrOrURL

    from vkbottle.modules import JSONModule


class AiohttpRequestKwargs(TypedDict, total=False):
    """https://github.com/aio-libs/aiohttp/blob/33953f110e97eecc707e1402daa8d543f38a189b/aiohttp/client.py#L369"""

    params: Mapping[str, str | int] | str | None
    json: Any
    cookies: LooseCookies | None
    headers: LooseHeaders | None
    skip_auto_headers: Iterable[str] | None
    auth: BasicAuth | None
    allow_redirects: bool
    max_redirects: int
    compress: str | None
    chunked: bool | None
    expect100: bool
    raise_for_status: None | bool | Callable[[ClientResponse], Awaitable[None]]
    read_until_eof: bool
    proxy: StrOrURL | None
    proxy_auth: BasicAuth | None
    timeout: ClientTimeout | None
    ssl: SSLContext | bool | Fingerprint
    server_hostname: str | None
    proxy_headers: LooseHeaders | None
    trace_request_ctx: Mapping[str, str] | None
    read_bufsize: int | None
    auto_decompress: bool | None
    max_line_size: int | None
    max_field_size: int | None


class AiohttpSessionKwargs(TypedDict, total=False):
    """https://github.com/aio-libs/aiohttp/blob/33953f110e97eecc707e1402daa8d543f38a189b/aiohttp/client.py#L199"""

    base_url: StrOrURL | None
    connector: BaseConnector | None
    loop: AbstractEventLoop | None
    cookies: LooseCookies | None
    headers: LooseHeaders | None
    skip_auto_headers: Iterable[str] | None
    auth: BasicAuth | None

    # Пришлось изменить из-за реализации AiohttpClient
    json_serialize: JSONModule

    request_class: type[ClientRequest]
    response_class: type[ClientResponse]
    ws_response_class: type[ClientWebSocketResponse]
    version: HttpVersion
    cookie_jar: AbstractCookieJar | None
    connector_owner: bool
    raise_for_status: bool
    read_timeout: float | object
    conn_timeout: float | None
    timeout: object | ClientTimeout
    auto_decompress: bool
    trust_env: bool
    requote_redirect_url: bool
    trace_configs: list[TraceConfig] | None
    read_bufsize: int


__all__ = ("AiohttpRequestKwargs", "AiohttpSessionKwargs")
