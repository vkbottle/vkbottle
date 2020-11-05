from vkbottle import API, VKAPIError, ABCRequestRescheduler, CtxStorage, ABCAPIErrorHandler, ABCAPI
from vkbottle.tools.test_utils import with_mocked_api
import pytest
import typing


USERS_GET_RESPONSE = (
    '{"response":[{"first_name":"Павел","id":1,"last_name":"Дуров",'
    '"can_access_closed":true,"is_closed":false}]}'
)
ctx_storage = CtxStorage()


class MockedRescheduler(ABCRequestRescheduler):
    def __init__(self, recent_response: typing.Any, final_response: dict):
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
    response = await api.users.get(1)

    assert isinstance(response, list)
    assert response[0].first_name == "Павел"


@pytest.mark.asyncio
@with_mocked_api('{"error":{"error_code":0,"error_msg":"Some Error!"}}')
async def test_api_error_handling(api: API):
    try:
        await api.request("some.method", {})
    except VKAPIError(0):
        return True
    raise AssertionError


@pytest.mark.asyncio
@with_mocked_api(None)
async def test_api_invalid_response(api: API):
    api.request_rescheduler = MockedRescheduler(None, {"some": "response"})
    response = await api.request("some.method", {})
    assert response == {"some": "response"}


@pytest.mark.asyncio
@with_mocked_api(1)
async def test_response_validators(api: API):
    api.response_validators = []
    assert await api.request("some.method", {}) == 1


@pytest.mark.asyncio
@with_mocked_api('{"error":{"error_code":5,"error_msg":"Some error occurred!"}}')
async def test_api_error_handler(api: API):
    async def error_handler(e: VKAPIError, data: dict):
        ctx_storage.set("error_handler_checked", True)
        assert e.code == 5
        assert data["method"] == "some.method"
        assert data["ctx_api"] == api

    api.api_error_handler.register_api_error_handler(5, error_handler)

    await api.request("some.method", {})
    assert ctx_storage.get("error_handler_checked")


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
@with_mocked_api('{"error":{"error_code":6,"error_msg":"Whoops"}}')
async def test_abc_error_handler(api: API):
    class CustomErrHandler(ABCAPIErrorHandler):
        def register_api_error_handler(self, code: int, error_handler):
            ctx_storage.set(f"error-{code}", error_handler)

        async def handle_error(self, code: int, description: str, data: dict):
            handler = ctx_storage.get(f"error-{code}")
            assert handler
            assert data["ctx_api"] == api
            assert data["method"] == "some.cool_method"
            assert data["data"]["a"] == 1
            assert await handler(VKAPIError(code, description), data)

    api.api_error_handler = CustomErrHandler()

    @api.api_error_handler.api_error_handler(6)
    async def error_handler(e: VKAPIError, data: dict):
        return True

    await api.request("some.cool_method", {"a": 1})


@pytest.mark.asyncio
async def test_types_translator():
    api = API("token")
    assert await api.validate_request({"a": [1, 2, 3, 4, "hi!"]}) == {"a": "1,2,3,4,hi!"}
