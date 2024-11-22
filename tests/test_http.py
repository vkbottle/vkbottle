import pytest

from tests.test_utils import MockedClient
from vkbottle.http import AiohttpClient


@pytest.mark.asyncio
async def test_client():
    client = MockedClient("some text")
    text = await client.request_text("https://example.com")
    await client.close()
    assert text == "some text"


@pytest.mark.asyncio
async def test_client_init():
    client = AiohttpClient(test="test")  # type: ignore
    assert client._session_params["test"] == "test"  # type: ignore
