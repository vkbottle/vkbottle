import pytest
from aiohttp.client_reqrep import ClientResponse
from aioresponses import aioresponses


class _NoopStreamWriter:
    # aiohttp 3.14 reads only `output_size` off the stream writer when the request
    # has already been sent (writer is None) — which is how aioresponses builds its
    # mocked responses.
    output_size = 0


@pytest.fixture
def mock_aioresponse():
    original_init = ClientResponse.__init__

    def patched_init(self, *args, **kwargs):
        # aioresponses 0.7.8 (latest release) doesn't pass the `stream_writer`
        # keyword that aiohttp 3.14 made required; supply a no-op default so the
        # mocked responses can still be constructed. The guard keeps real aiohttp
        # responses (which pass their own writer) untouched.
        if "stream_writer" not in kwargs:
            kwargs["stream_writer"] = _NoopStreamWriter()
        original_init(self, *args, **kwargs)

    ClientResponse.__init__ = patched_init
    try:
        with aioresponses() as m:
            yield m
    finally:
        ClientResponse.__init__ = original_init
