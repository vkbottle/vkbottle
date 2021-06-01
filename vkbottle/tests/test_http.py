import pytest

from vkbottle import ManySessionManager
from vkbottle.tools.test_utils import MockedClient


@pytest.mark.asyncio
async def test_client():
    client = MockedClient("some text")
    text = await client.request_text("GET", "https://example.com")
    await client.close()
    assert text == "some text"


@pytest.mark.asyncio
async def test_session_manager():
    session_manager = ManySessionManager(lambda: MockedClient("some text"))
    async with session_manager as session:
        assert await session.request_text("GET", "https://example.com") == "some text"
