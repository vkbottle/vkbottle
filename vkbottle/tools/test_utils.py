from typing import Any, Callable, Optional

from vkbottle import API, ABCClient, ABCResponse


class MockedResponse(ABCResponse):
    def __init__(self, return_value: Any):
        self.return_value = return_value

    def text(self) -> str:
        return self.return_value

    def content(self) -> bytes:
        return self.return_value

    def json(self) -> Any:
        return self.return_value


class MockedClient(ABCClient):
    def __init__(self, return_value: Optional[Any] = None, callback: Optional[Callable] = None):
        self.return_value = return_value
        self.callback = callback or (lambda method, url, data: None)

    async def request(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> MockedResponse:
        return MockedResponse(self.return_value or self.callback(method, url, data))


def with_mocked_api(return_value: Any):
    """Just changes http standard api client to mocked client which returns return_value"""

    def decorator(func: Any):
        async def wrapper(*args, **kwargs):
            api = API("token")
            api.http_client = MockedClient(return_value)
            return await func(*args, **kwargs, api=api)

        return wrapper

    return decorator
