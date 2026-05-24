import json
from typing import Any

import pytest

from tests.test_utils import MockedClient
from vkbottle import API, ABCHTTPClient, Bot
from vkbottle.polling.bot_polling import BotPolling

EXAMPLE_EVENT = {
    "ts": 1,
    "updates": [
        {
            "type": "message_new",
            "object": {},
        },
    ],
}


@pytest.fixture(autouse=True)
def polling_state_tmp_path(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)


def make_bot_polling() -> tuple[BotPolling, API]:
    call_count = 0

    def callback(method: str, url: str, data: dict[str, Any]):
        nonlocal call_count

        if "groups.getById" in url:
            return {"response": {"groups": [{"id": 1}]}}
        if "groups.getLongPollServer" in url:
            return {"response": {"ts": 1, "server": "!SERVER!", "key": ""}}
        if "!SERVER!" in url:
            call_count += 1
            return {**EXAMPLE_EVENT, "ts": call_count}

        return {}

    api = API("token")
    api.http_client = MockedClient(callback=callback)

    polling = BotPolling(api=api)
    return polling, api


class TrackingClient(ABCHTTPClient):
    def __init__(self) -> None:
        self.longpoll_requests: list[dict[str, Any]] = []
        self.longpoll_timeouts: list[Any] = []

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if "groups.getById" in url:
            return {"response": {"groups": [{"id": 1}]}}
        if "groups.getLongPollServer" in url:
            return {"response": {"ts": 1, "server": "!SERVER!", "key": "key+with=sig"}}
        return {}

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if url != "!SERVER!":
            return {}

        self.longpoll_requests.append(kwargs["params"])
        self.longpoll_timeouts.append(kwargs["timeout"])
        if len(self.longpoll_requests) == 1:
            return {"ts": 2, "updates": []}
        return {**EXAMPLE_EVENT, "ts": 3}

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        return {}

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> bytes:
        return b""

    async def close(self) -> None:
        pass


class OldEventsClient(ABCHTTPClient):
    def __init__(self, server_ts: int, event_ts: int) -> None:
        self.server_ts = server_ts
        self.event_ts = event_ts
        self.longpoll_requests: list[dict[str, Any]] = []

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if "groups.getById" in url:
            return {"response": {"groups": [{"id": 1}]}}
        if "groups.getLongPollServer" in url:
            return {"response": {"ts": self.server_ts, "server": "!SERVER!", "key": ""}}
        return {}

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if url != "!SERVER!":
            return {}

        self.longpoll_requests.append(kwargs["params"])
        return {**EXAMPLE_EVENT, "ts": self.event_ts}

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        return {}

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> bytes:
        return b""

    async def close(self) -> None:
        pass


@pytest.mark.asyncio
async def test_stop_terminates_listen():
    """stop() should terminate the listen() loop."""
    polling, _ = make_bot_polling()
    events = []

    async for event in polling.listen():
        events.append(event)
        polling.stop()

    assert len(events) == 1
    assert events[0]["updates"] == EXAMPLE_EVENT["updates"]


@pytest.mark.asyncio
async def test_listen_works_after_stop():
    """listen() should work again after a previous stop()."""
    polling, _ = make_bot_polling()

    async for _event in polling.listen():
        polling.stop()
        break

    events = []

    async for event in polling.listen():
        events.append(event)
        polling.stop()

    assert len(events) == 1


@pytest.mark.asyncio
async def test_stop_before_listen_is_noop():
    """Calling stop() before listen() should not raise."""
    polling, _ = make_bot_polling()
    polling.stop()

    events = []

    async for event in polling.listen():
        events.append(event)
        polling.stop()

    assert len(events) == 1


@pytest.mark.asyncio
async def test_empty_updates_advance_ts_without_yielding():
    """Empty longpoll responses should move ts but not be exposed as events."""

    client = TrackingClient()
    api = API("token")
    api.http_client = client
    polling = BotPolling(api=api, wait=25)

    events = []
    async for event in polling.listen():
        events.append(event)
        polling.stop()

    assert events == [{**EXAMPLE_EVENT, "ts": 3}]
    assert [request["ts"] for request in client.longpoll_requests] == [1, 2]
    assert client.longpoll_requests[0]["key"] == "key+with=sig"
    assert all(timeout.total == 35 for timeout in client.longpoll_timeouts)


def test_bot_passes_old_events_settings_to_polling():
    bot = Bot(token="token", skip_old_events=False)

    assert bot.skip_old_events is False
    assert isinstance(bot.polling, BotPolling)
    assert bot.polling.skip_old_events is False


def test_bot_skips_old_events_by_default():
    bot = Bot(token="token")

    assert bot.skip_old_events is True
    assert isinstance(bot.polling, BotPolling)
    assert bot.polling.skip_old_events is True


@pytest.mark.asyncio
async def test_bot_polling_saves_ts_when_skipping_old_events():
    client = OldEventsClient(server_ts=10, event_ts=11)
    api = API("token")
    api.http_client = client
    polling = BotPolling(api=api)

    async for _event in polling.listen():
        polling.stop()

    assert client.longpoll_requests[0]["ts"] == 10
    assert json.loads(polling.ts_state_path.read_text(encoding="utf-8")) == {"ts": 11}


@pytest.mark.asyncio
async def test_bot_polling_restores_old_events_ts(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    first_client = OldEventsClient(server_ts=1, event_ts=2)
    first_api = API("token")
    first_api.http_client = first_client
    first_polling = BotPolling(api=first_api, skip_old_events=False)

    async for _event in first_polling.listen():
        first_polling.stop()

    assert first_client.longpoll_requests[0]["ts"] == 1

    second_client = OldEventsClient(server_ts=10, event_ts=11)
    second_api = API("token")
    second_api.http_client = second_client
    second_polling = BotPolling(api=second_api, skip_old_events=False)

    async for _event in second_polling.listen():
        second_polling.stop()

    assert second_client.longpoll_requests[0]["ts"] == 2
