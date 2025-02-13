from __future__ import annotations

from collections.abc import Awaitable, Iterable, Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    List,
    Optional,
    Type,
    Union,
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

    params: Union[Mapping[str, Union[str, int]], str, None]
    json: Any
    cookies: Union[LooseCookies, None]
    headers: Union[LooseHeaders, None]
    skip_auto_headers: Union[Iterable[str], None]
    auth: Union[BasicAuth, None]
    allow_redirects: bool
    max_redirects: int
    compress: Union[str, None]
    chunked: Union[bool, None]
    expect100: bool
    raise_for_status: Union[None, bool, Callable[[ClientResponse], Awaitable[None]]]
    read_until_eof: bool
    proxy: Union[StrOrURL, None]
    proxy_auth: Union[BasicAuth, None]
    timeout: "Union[ClientTimeout, None]"
    ssl: Union[SSLContext, bool, Fingerprint]
    server_hostname: Union[str, None]
    proxy_headers: Union[LooseHeaders, None]
    trace_request_ctx: Union[Mapping[str, str], None]
    read_bufsize: Union[int, None]
    auto_decompress: Union[bool, None]
    max_line_size: Union[int, None]
    max_field_size: Union[int, None]


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


__all__ = ("AiohttpRequestKwargs", "AiohttpSessionKwargs")
