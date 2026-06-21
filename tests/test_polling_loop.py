import pytest
from aiohttp.client_exceptions import ClientConnectionError

from vkbottle.exception_factory import ErrorHandler
from vkbottle.polling.base import BasePolling


class _Polling(BasePolling):
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.server_calls = 0
        self.event_calls = 0

    def construct(self, *args, **kwargs):
        return self

    @property
    def api(self):
        return None

    async def get_server(self):
        self.server_calls += 1
        return {"server": "s", "key": "k", "ts": "100"}

    async def get_event(self, server):
        self.event_calls += 1
        if self.event_calls == 1:
            msg = "transient blip"
            raise ClientConnectionError(msg)
        self.stop()
        return {"ts": "101", "updates": [{"x": 1}]}


@pytest.mark.asyncio
async def test_polling_keeps_ts_on_transient_error(mocker):
    # Don't actually sleep through the back-off.
    mocker.patch("asyncio.sleep")

    polling = _Polling()
    events = [event async for event in polling.listen()]

    # The transient error must not discard the server/ts and refetch a fresh server
    # (which would skip every event queued between the old ts and "now").
    assert polling.server_calls == 1
    assert events == [{"ts": "101", "updates": [{"x": 1}]}]
