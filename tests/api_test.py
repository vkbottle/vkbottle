import pytest

from vkbottle import API


def skippable_api_test(func):
    async def wrapper(api: API):
        if not api.token:
            return pytest.skip("TOKEN is not set as enviroment variable")
        return await func(api)

    return wrapper


@pytest.mark.asyncio
@skippable_api_test
async def test_api_response(api: API):
    response = await api.request("users.get", {"user_ids": 1})
    assert isinstance(response, dict)
    assert isinstance(response["response"], list)
    assert response["response"][0]["first_name"] == "Павел"


@pytest.mark.asyncio
@skippable_api_test
async def test_api_typed_response(api: API):
    response = await api.users.get(1)
    assert isinstance(response, list)
    assert response[0].first_name == "Павел"
