from typing import Any

import pytest

from vkbottle import API, ABCRequestRescheduler, CaptchaError, CtxStorage, VKAPIError
from tests.test_utils import with_mocked_api

USERS_GET_RESPONSE = (
    '{"response":[{"first_name":"Павел","id":1,"last_name":"Дуров",'
    '"can_access_closed":true,"is_closed":false}]}'
)
ctx_storage = CtxStorage()


class MockedRescheduler(ABCRequestRescheduler):
    def __init__(self, recent_response: Any, final_response: dict):
        self.recent_response = recent_response
        self.final_response = final_response

    async def reschedule(self, *args) -> dict:
        assert args[3] == self.recent_response
        return self.final_response


@pytest.mark.asyncio
@with_mocked_api(USERS_GET_RESPONSE)
async def test_api_raw_response(api: API):
    response = await api.request("users.get", {"user_ids": 1})

    assert isinstance(response["response"], list)
    assert response["response"][0]["first_name"] == "Павел"


@pytest.mark.asyncio
@with_mocked_api(USERS_GET_RESPONSE)
async def test_api_typed_response(api: API):
    response = await api.users.get(1)  # type: ignore

    assert isinstance(response, list)
    assert response[0].first_name == "Павел"


@pytest.mark.asyncio
@with_mocked_api('{"error":{"error_code":0,"error_msg":"Some Error!","request_params":[]}}')
async def test_vk_api_error_handling(api: API):
    try:
        await api.request("some.method", {})
    except VKAPIError[0]:
        return True
    raise AssertionError


@pytest.mark.asyncio
@with_mocked_api(
    '{"error":{"error_code":14,"error_msg":"Captcha needed","request_params":'
    '[{"key":"oauth","value":"1"},{"key":"method","value":"captcha.force"},{"key":"uids",'
    '"value":"66748"},{"key":"access_token","value":'
    '"b9b5151856dcc745d785a6b604295d30888a827a37763198888d8b7f5271a4d8a049fefbaeed791b2882"}],'
    '"captcha_sid":"239633676097","captcha_img":"https://api.vk.com/captcha.php?'
    'sid=239633676097&s=1"}}'
)
async def test_captcha_error_handling(api: API):
    try:
        await api.request("some.method", {})
    except VKAPIError as e:
        assert isinstance(e, CaptchaError)
        assert e.code == 14
        assert e.sid == 239633676097


@pytest.mark.asyncio
@with_mocked_api(None)
async def test_api_invalid_response(api: API):
    api.request_rescheduler = MockedRescheduler(None, {"response": {"some": "response"}})
    response = await api.request("some.method", {})
    assert response == {"response": {"some": "response"}}


@pytest.mark.asyncio
@with_mocked_api(1)
async def test_response_validators(api: API):
    api.response_validators = []
    assert await api.request("some.method", {}) == 1


@pytest.mark.asyncio
@with_mocked_api('{"error":{"error_code":5,"error_msg":"Some error occurred!"}}')
async def test_ignore_errors(api: API):
    api.ignore_errors = True
    assert await api.request("some.method", {}) is None


@pytest.mark.asyncio
@with_mocked_api('{"response":1}')
async def test_request_many(api: API):
    i = 0
    async for response in api.request_many(
        [api.APIRequest("some.method", {}), api.APIRequest("some.method", {})]
    ):
        assert response == {"response": 1}
        i += 1
    assert i == 2


@pytest.mark.asyncio
async def test_types_translator():
    api = API("token")
    assert await api.validate_request({"a": [1, 2, 3, 4, "hi!"]}) == {"a": "1,2,3,4,hi!"}


@pytest.mark.asyncio
@with_mocked_api('{"error": {"error_code": 10, "error_msg": "Internal server error: Unknown error, try later"}}')
async def test_error_handling_without_request_params(api: API):
    try:
        await api.request("some.method", {})
    except VKAPIError[10]:
        return True
    raise AssertionError
