import asyncio

import pytest

from vkbottle import ABCEventDeduplicator, Bot, MemoryEventDeduplicator

EVENT = {
    "type": "message_new",
    "object": {"message": {"id": 42, "peer_id": 1, "text": "hello"}},
    "group_id": 1,
}


@pytest.mark.asyncio
async def test_dual_mode_claims_same_event_once_from_both_transports():
    bot = Bot(token="token", dual_mode=True, event_deduplicator=MemoryEventDeduplicator())
    processed: list[dict] = []

    async def route(event, api):
        await asyncio.sleep(0)
        processed.append(event)

    bot.router.route = route

    await asyncio.gather(
        bot.process_event({**EVENT, "event_id": "callback-id", "secret": "secret"}),
        bot.process_event(EVENT),
    )

    assert len(processed) == 1
    assert processed[0]["object"] == EVENT["object"]


@pytest.mark.asyncio
async def test_dual_mode_allows_distinct_events():
    bot = Bot(token="token", dual_mode=True, event_deduplicator=MemoryEventDeduplicator())
    processed: list[dict] = []

    async def route(event, api):
        processed.append(event)

    bot.router.route = route
    await bot.process_event(EVENT)
    await bot.process_event({**EVENT, "object": {"message": {"id": 43}}})

    assert len(processed) == 2


@pytest.mark.asyncio
async def test_deduplication_is_disabled_by_default():
    bot = Bot(token="token")
    processed: list[dict] = []

    async def route(event, api):
        processed.append(event)

    bot.router.route = route
    await bot.process_event(EVENT)
    await bot.process_event(EVENT)

    assert len(processed) == 2


@pytest.mark.asyncio
async def test_uses_custom_event_deduplicator():
    class EventDeduplicator(ABCEventDeduplicator):
        async def claim(self, event: dict) -> bool:
            return False

    bot = Bot(token="token", event_deduplicator=EventDeduplicator())
    processed: list[dict] = []

    async def route(event, api):
        processed.append(event)

    bot.router.route = route
    await bot.process_event(EVENT)

    assert processed == []
