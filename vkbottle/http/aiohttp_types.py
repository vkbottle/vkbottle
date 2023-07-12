from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, List, Mapping, Optional, Type, Union

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from ssl import SSLContext
    from types import SimpleNamespace

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


class AiohttpSessionKwargs(TypedDict, total=False):
    """https://github.com/aio-libs/aiohttp/blob/33953f110e97eecc707e1402daa8d543f38a189b/aiohttp/client.py#L199"""

    base_url: Optional[StrOrURL]
    connector: Optional[BaseConnector]
    loop: Optional[AbstractEventLoop]
    cookies: Optional[LooseCookies]
    headers: Optional[LooseHeaders]
    skip_auto_headers: Optional[Iterable[str]]
    auth: Optional[BasicAuth]

    # Пришлось изменить из-за реализации AiohttpClient
    json_serialize: JSONModule

    request_class: Type[ClientRequest]
    response_class: Type[ClientResponse]
    ws_response_class: Type[ClientWebSocketResponse]
    version: HttpVersion
    cookie_jar: Optional[AbstractCookieJar]
    connector_owner: bool
    raise_for_status: bool
    read_timeout: Union[float, object]
    conn_timeout: Optional[float]
    timeout: Union[object, ClientTimeout]
    auto_decompress: bool
    trust_env: bool
    requote_redirect_url: bool
    trace_configs: Optional[List[TraceConfig]]
    read_bufsize: int


class AiohttpRequestKwargs(TypedDict, total=False):
    """https://github.com/aio-libs/aiohttp/blob/33953f110e97eecc707e1402daa8d543f38a189b/aiohttp/client.py#L369"""

    params: Optional[Mapping[str, str]]

    # Методы ABCHTTPClient уже принимают data
    # data: Any

    json: Any
    cookies: Optional[LooseCookies]
    headers: Optional[LooseHeaders]
    skip_auto_headers: Optional[Iterable[str]]
    auth: Optional[BasicAuth]
    allow_redirects: bool
    max_redirects: int
    compress: Optional[str]
    chunked: Optional[bool]
    expect100: bool
    raise_for_status: Optional[bool]
    read_until_eof: bool
    proxy: Optional[StrOrURL]
    proxy_auth: Optional[BasicAuth]
    timeout: Union[ClientTimeout, object]
    verify_ssl: Optional[bool]
    fingerprint: Optional[bytes]
    ssl_context: Optional[SSLContext]
    ssl: Optional[Union[SSLContext, bool, Fingerprint]]
    proxy_headers: Optional[LooseHeaders]
    trace_request_ctx: Optional[SimpleNamespace]
    read_bufsize: Optional[int]
