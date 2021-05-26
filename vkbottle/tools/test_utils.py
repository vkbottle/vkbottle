from typing import Any, Callable, Optional

from vkbottle import API, ABCHTTPClient


class MockedClient(ABCHTTPClient):
    def __init__(self, return_value: Optional[Any] = None, callback: Optional[Callable] = None):
        super().__init__()
        self.return_value = return_value
        self.callback = callback or (lambda data: None)

    async def request_text(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> str:
        return self.return_value or self.callback(locals())

    async def request_json(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> dict:
        return self.return_value or self.callback(locals())

    async def request_content(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> bytes:
        return self.return_value or self.callback(locals())

    async def close(self) -> None:
        pass


def with_mocked_api(return_value: Any):
    """ Just changes http standard api client to mocked client which returns return_value
    """

    def decorator(func: Any):
        async def wrapper(*args, **kwargs):
            api = API("token")
            api.http._session = MockedClient(return_value)
            return await func(*args, **kwargs, api=api)

        return wrapper

    return decorator
