import pytest

from vkbottle.tools.test_utils import MockedClient


@pytest.mark.asyncio
async def test_client():
    client = MockedClient("some text")
    text = await client.request_text("https://example.com")
    await client.close()
    assert text == "some text"
