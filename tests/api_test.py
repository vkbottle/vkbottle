from vkbottle.api import API
import pytest


@pytest.mark.asyncio
async def test_api_response(api: API):
    response = await api.request("users.get", {"user_ids": 1})
    assert isinstance(response, list)
    assert response[0]["first_name"] == "Павел"
