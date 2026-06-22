import types

import pytest

from vkbottle.dispatch.rules.base import CommandRule, CoroutineRule


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


@pytest.mark.asyncio
async def test_command_rule_respects_word_boundary():
    rule = CommandRule(("he", 2))
    # "/hello world" is command "hello", not "he" followed by args — must not match.
    assert await rule.check(_msg("/hello world")) is False
    # A real "/he a b" still matches with its two args.
    assert await rule.check(_msg("/he a b")) == {"args": ["a", "b"]}


@pytest.mark.asyncio
async def test_command_rule_allows_empty_string_args():
    rule = CommandRule(("set", 2))
    # A trailing empty argument is still a valid argument; it must not be dropped
    # by an all(args) truthiness check.
    assert await rule.check(_msg("/set a ")) == {"args": ["a", ""]}
