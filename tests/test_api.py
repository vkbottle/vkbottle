import asyncio
import json
from typing import Any

import pydantic
import pytest

from tests.test_utils import with_mocked_api
from vkbottle import API, ABCRequestRescheduler, APIAuthError, CaptchaError, CtxStorage, VKAPIError

USERS_GET_RESPONSE = (
    '{"response":[{"first_name":"Павел","id":1,"last_name":"Дуров",'
    '"can_access_closed":true,"is_closed":false}]}'
)
ctx_storage = CtxStorage()


class MockedRescheduler(ABCRequestRescheduler):
    def __init__(self, recent_response: Any, final_response: dict[str, Any]):
        self.recent_response = recent_response
        self.final_response = final_response

    async def reschedule(self, *args: Any) -> dict[str, Any]:
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
    '"captcha_sid":"239633676097","captcha_img":"https://api.vk.ru/captcha.php?'
    'sid=239633676097&s=1"}}'
)
async def test_captcha_error_handling(api: API):
    with pytest.raises(VKAPIError) as e:
        await api.request("some.method", {})
    assert isinstance(e.value, CaptchaError)
    assert e.value.code == 14
    assert e.value.captcha_sid == "239633676097"


@with_mocked_api(
    '{"error": {"error_code":5, '
    '"error_msg": "User authorization failed: user is blocked.", '
    '"request_params": [{"key": "v", "value": "5.199"}, '
    '{"key": "method", "value": "wall.getById"}, '
    '{"key": "oauth", "value": "1"}, '
    '{"key": "posts", "value": "123_123"}], '
    '"ban_info": {"member_name": "Test", "message": "Your account has been blocked", '
    '"access_token": "test_token"}}}'
)
async def test_auth_blocked_user_error_handling(api: API):
    with pytest.raises(VKAPIError) as e:
        await api.request("some.method", {})

    assert isinstance(e.value, APIAuthError)
    assert e.value.code == 5
    assert e.value.ban_info == {
        "member_name": "Test",
        "message": "Your account has been blocked",
        "access_token": "test_token",
    }


@pytest.mark.asyncio
@with_mocked_api(
    '{"error": {"error_code":5, '
    '"error_msg": "User authorization failed: invalid access_token (4).", '
    '"request_params": [{"key": "v", "value": "5.199"}, '
    '{"key": "method", "value": "wall.getById"},'
    ' {"key": "oauth", "value": "1"}, '
    '{"key": "posts", "value": "123_123"}]}}'
)
async def test_auth_error_handling(api: API):
    with pytest.raises(VKAPIError) as e:
        await api.request("some.method", {})
    assert isinstance(e.value, APIAuthError)
    assert e.value.code == 5
    assert not e.value.ban_info


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
@with_mocked_api(
    '{"error": {"error_code": 10, "error_msg": "Internal server error: Unknown error, try later"}}',
)
async def test_error_handling_without_request_params(api: API):
    try:
        await api.request("some.method", {})
    except VKAPIError[10]:
        return True
    raise AssertionError


def test_unexpected_kwargs_in_api_error():
    with pytest.raises(VKAPIError) as e:
        raise VKAPIError[5](
            error_msg="msg",
            unexpected_kwarg=123,
        )
    assert e.value.code == 5
    assert isinstance(e.value, APIAuthError)
    assert e.value.kwargs == {"unexpected_kwarg": 123}


@pytest.mark.asyncio
async def test_request_validator_serializes_pydantic_model():
    class _Model(pydantic.BaseModel):
        a: int
        items: list[int]

    api = API("token")
    result = await api.validate_request({"m": _Model(a=1, items=[1, 2, 3])})

    # A pydantic model must be serialized to a JSON *string*, like a dict — not
    # left as a raw dict that aiohttp's form encoder would mangle.
    assert isinstance(result["m"], str)
    assert json.loads(result["m"]) == {"a": 1, "items": [1, 2, 3]}


@pytest.mark.asyncio
async def test_json_validator_reschedule_guard_is_per_request():
    # The default JSONResponseValidator is a single instance shared by every API,
    # so its reschedule re-entrancy guard must be per-request, not process-global.
    from vkbottle.api.response_validator import JSONResponseValidator

    validator = JSONResponseValidator()

    a_inside = asyncio.Event()
    release_a = asyncio.Event()

    class _ReschedA:
        async def reschedule(self, ctx_api, method, data, recent):
            a_inside.set()
            await release_a.wait()
            return {"response": "A"}

    class _ReschedB:
        async def reschedule(self, ctx_api, method, data, recent):
            return {"response": "B"}

    class _Api:
        def __init__(self, rescheduler):
            self.request_rescheduler = rescheduler

    # Request A gets an invalid (non-dict/str) response and parks inside its reschedule.
    task_a = asyncio.create_task(validator.validate("m", {}, object(), _Api(_ReschedA())))
    await a_inside.wait()

    # Request B also gets an invalid response: it must reschedule itself, not observe
    # A's in-flight reschedule flag and silently return None.
    result_b = await validator.validate("m", {}, object(), _Api(_ReschedB()))

    release_a.set()
    result_a = await task_a

    assert result_b == {"response": "B"}
    assert result_a == {"response": "A"}


@pytest.mark.asyncio
async def test_blocking_rescheduler_uses_async_sleep(mocker):
    from unittest.mock import AsyncMock

    from vkbottle.api.request_rescheduler.blocking import BlockingRequestRescheduler

    # A blocking time.sleep in an async rescheduler stalls the whole event loop;
    # it must await asyncio.sleep instead.
    async_sleep = mocker.patch("asyncio.sleep", new=AsyncMock())

    class _Api:
        async def request(self, method, data):
            return {"response": 1}

    result = await BlockingRequestRescheduler(delay=0).reschedule(
        _Api(), "m", {}, recent_response=None
    )

    assert result == {"response": 1}
    async_sleep.assert_awaited()
