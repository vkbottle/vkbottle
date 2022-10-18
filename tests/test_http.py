import pytest

from vkbottle.http import AiohttpClient, SingleAiohttpClient
from tests.test_utils import MockedClient


@pytest.mark.asyncio
async def test_client():
    client = MockedClient("some text")
    text = await client.request_text("https://example.com")
    await client.close()
    assert text == "some text"


@pytest.mark.asyncio
async def test_client_init():
    client = AiohttpClient(test="test")
    assert client._session_params["test"] == "test"
    singleton_client = SingleAiohttpClient(test="test")
    assert singleton_client._session_params["test"] == "test"
