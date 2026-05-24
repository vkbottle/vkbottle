import asyncio
from typing import Any

import pytest

from vkbottle.tools.mini_types.user.message import message_min


class Response:
    def __init__(self, items: list[Any]) -> None:
        self.items = items


class MessageItem:
    def model_dump(self) -> dict[str, Any]:
        return {
            "peer_id": 1,
            "date": 1,
            "from_id": 1,
            "text": "test",
            "out": 0,
            "id": 42,
            "conversation_message_id": 1,
            "version": 1,
            "fwd_messages": [],
        }


class Messages:
    def __init__(self, responses: list[Response]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []

    async def get_by_id(self, **data: Any) -> Response:
        self.calls.append(data)
        return self.responses.pop(0)


class API:
    def __init__(self, responses: list[Response]) -> None:
        self.messages = Messages(responses)


@pytest.mark.asyncio
async def test_user_message_min_retries_empty_get_by_id_response() -> None:
    api = API([Response([]), Response([MessageItem()])])

    message = await message_min(42, api, fetch_attempts=2, fetch_retry_delay=0)

    assert message.id == 42
    assert api.messages.calls == [{"message_ids": [42]}, {"message_ids": [42]}]


@pytest.mark.asyncio
async def test_user_message_min_cancels_when_retries_are_exhausted() -> None:
    api = API([Response([]), Response([])])

    with pytest.raises(asyncio.CancelledError):
        await message_min(42, api, fetch_attempts=2, fetch_retry_delay=0)

    assert api.messages.calls == [{"message_ids": [42]}, {"message_ids": [42]}]
