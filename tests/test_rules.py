import types

import pytest

from vkbottle.dispatch.rules.base import CoroutineRule


def _msg(text: str):
    return types.SimpleNamespace(text=text)


@pytest.mark.asyncio
async def test_coroutine_rule_is_reusable_across_events():
    calls = {"n": 0}

    async def make():
        calls["n"] += 1
        return True

    rule = CoroutineRule(make)
    # A rule instance is checked against every event; a one-shot coroutine would
    # raise "cannot reuse already awaited coroutine" on the second event.
    assert await rule.check(_msg("a")) is True
    assert await rule.check(_msg("b")) is True
    assert calls["n"] == 2
