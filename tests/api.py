from vkbottle.api import API
import pytest

@pytest.mark.asyncio
async def test_api_response(api: API):
    response = await api.request("users.get", {})
    assert isinstance(response, dict)
    assert response["first_name"] == "Павел"
