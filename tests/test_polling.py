import pytest

from tests.test_utils import MockedClient
from vkbottle import API
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


def make_bot_polling() -> tuple[BotPolling, API]:
    call_count = 0

    def callback(method: str, url: str, data: dict):
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
