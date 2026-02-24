from typing import Any

import pytest

from tests.test_utils import MockedClient
from vkbottle import API
from vkbottle.tools.mini_types.bot.foreign_message import ForeignMessageMin


def fake_foreign_message(ctx_api: API, **data: Any) -> ForeignMessageMin:
    message = {
        "peer_id": 1,
        "date": 1,
        "from_id": 1,
        "text": "short",
        "conversation_message_id": 42,
        "fwd_messages": [],
    }

    message.update(data)
    return ForeignMessageMin(
        **message,
        unprepared_ctx_api=ctx_api,
        replace_mention=True,
        group_id=1,
    )


def _make_api_with_callback(callback):
    api = API("token")
    api.http_client = MockedClient(callback=callback)
    return api


@pytest.mark.asyncio
async def test_get_full_message():
    call_count = 0

    def callback(method: str, url: str, data: dict):
        nonlocal call_count
        if "messages.getByConversationMessageId" in url:
            call_count += 1
            return {
                "response": {
                    "count": 1,
                    "items": [
                        {
                            "peer_id": 1,
                            "date": 1,
                            "from_id": 1,
                            "text": "full message text with all attachments",
                            "conversation_message_id": 42,
                            "id": 100,
                            "out": 0,
                            "version": 1,
                            "fwd_messages": [],
                            "attachments": [],
                        }
                    ],
                }
            }

    api = _make_api_with_callback(callback)
    msg = fake_foreign_message(api, text="short")

    result = await msg.get_full_message()

    assert result is msg
    assert msg.text == "full message text with all attachments"
    assert msg._is_full is True
    assert call_count == 1

    # Second call should use cache
    result2 = await msg.get_full_message()
    assert result2 is msg
    assert call_count == 1  # No additional API call


@pytest.mark.asyncio
async def test_get_full_message_with_explicit_peer_id():
    captured_data = {}

    def callback(method: str, url: str, data: dict):
        if "messages.getByConversationMessageId" in url:
            captured_data.update(data)
            return {
                "response": {
                    "count": 1,
                    "items": [
                        {
                            "peer_id": 999,
                            "date": 1,
                            "from_id": 1,
                            "text": "full text",
                            "conversation_message_id": 42,
                            "id": 100,
                            "out": 0,
                            "version": 1,
                            "fwd_messages": [],
                        }
                    ],
                }
            }

    api = _make_api_with_callback(callback)
    msg = fake_foreign_message(api, text="short", peer_id=1)

    await msg.get_full_message(peer_id=999)

    assert captured_data["peer_id"] == 999
