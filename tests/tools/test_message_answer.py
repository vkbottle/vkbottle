import pytest

from tests.test_utils import MockedClient
from vkbottle import API
from vkbottle.tools.mini_types.user.message import MessageMin


def _make_message(sent: list[dict]) -> MessageMin:
    def callback(method, url, data):
        sent.append(dict(data))
        return f'{{"response":[{{"peer_id":1,"message_id":{100 + len(sent)}}}]}}'

    api = API("token")
    api.http_client = MockedClient(callback=callback)
    return MessageMin(
        peer_id=1,
        date=1,
        from_id=1,
        text="",
        out=0,
        id=42,
        conversation_message_id=1,
        version=1,
        fwd_messages=[],
        unprepared_ctx_api=api,
    )


@pytest.mark.asyncio
async def test_answer_returns_first_chunk_response():
    sent: list[dict] = []
    message = _make_message(sent)

    result = await message.answer("a" * 5000)  # > 4096 -> two chunks

    assert len(sent) == 2
    # The primary (first) message id must be returned, not the last chunk's.
    assert result.message_id == 101


@pytest.mark.asyncio
async def test_answer_varies_random_id_per_chunk():
    sent: list[dict] = []
    message = _make_message(sent)

    await message.answer("a" * 5000, random_id=555)

    assert len(sent) == 2
    # A non-zero random_id must differ per chunk, or VK deduplicates and drops every
    # chunk after the first.
    assert sent[0]["random_id"] != sent[1]["random_id"]
