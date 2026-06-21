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


class _GenericErrorPolling(_Polling):
    async def get_event(self, server):
        self.event_calls += 1
        if self.event_calls == 1:
            msg = "boom"
            raise RuntimeError(msg)
        self.stop()
        return {"ts": "1", "updates": [{"x": 1}]}


@pytest.mark.asyncio
async def test_polling_backs_off_on_generic_error(mocker):
    sleep = mocker.patch("asyncio.sleep")

    polling = _GenericErrorPolling()
    _events = [event async for event in polling.listen()]

    # An unexpected exception must trigger a back-off, not spin tightly re-handling
    # the same error and flooding logs.
    sleep.assert_awaited()


class _UnknownFailurePolling(_Polling):
    async def get_event(self, server):
        self.event_calls += 1
        if self.event_calls == 1:
            return {"failed": 999}  # unknown failure code -> handle_failed_event returns {}
        self.stop()
        return {"ts": "1", "updates": [{"x": 1}]}


@pytest.mark.asyncio
async def test_polling_backs_off_on_unhandled_failure(mocker):
    sleep = mocker.patch("asyncio.sleep")

    polling = _UnknownFailurePolling()
    _events = [event async for event in polling.listen()]

    # An unhandled failure code yields an empty server; the loop must back off before
    # refetching instead of spinning a tight reconnect loop.
    sleep.assert_awaited()


@pytest.mark.asyncio
async def test_polling_saves_ts_after_event_processed():
    order = []

    class _OrderedPolling(_Polling):
        def save_server_ts(self, server):
            order.append(("save", server["ts"]))

        async def get_event(self, server):
            self.event_calls += 1
            if self.event_calls == 1:
                return {"ts": "5", "updates": [{"x": 1}]}
            self.stop()
            return {"ts": "6", "updates": []}

    polling = _OrderedPolling()
    async for event in polling.listen():
        ts = event["ts"]
        order.append(("process", ts))
        order.append(("processed", ts))

    # The ts for an event must be persisted only after the event was handed off, so a
    # crash mid-processing re-fetches the event instead of silently skipping it.
    assert order.index(("process", "5")) < order.index(("save", "5"))


class _SingleEventPolling(_Polling):
    async def get_event(self, server):
        self.event_calls += 1
        self.stop()
        return {"ts": "1", "updates": [{"x": 1}]}


@pytest.mark.asyncio
async def test_polling_saves_ts_off_the_event_loop(mocker):
    to_thread = mocker.patch("asyncio.to_thread")

    polling = _SingleEventPolling()
    _events = [event async for event in polling.listen()]

    # The (potentially blocking) ts save must be offloaded to a thread so it doesn't
    # block the event loop on every longpoll batch.
    to_thread.assert_awaited()
    assert to_thread.await_args.args[0] == polling.save_server_ts
