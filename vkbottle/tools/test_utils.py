from typing import Any, Callable, Optional, Union

from vkbottle import API, ABCHTTPClient


class MockedClient(ABCHTTPClient):
    def __init__(self, return_value: Optional[Any] = None, callback: Optional[Callable] = None):
        super().__init__()
        self.return_value = return_value
        self.callback = callback or (lambda method, url, data: None)

    async def request_raw(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> Union[str, Any]:
        return self.return_value or self.callback(method, url, data)

    async def request_text(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> Union[str, Any]:
        return self.return_value or self.callback(method, url, data)

    async def request_json(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> Union[dict, Any]:
        return self.return_value or self.callback(method, url, data)

    async def request_content(
        self, url: str, method: str = "GET", data: Optional[dict] = None, **kwargs
    ) -> Union[bytes, Any]:
        return self.return_value or self.callback(method, url, data)

    async def close(self) -> None:
        pass


def with_mocked_api(return_value: Any):
    """Just changes http standard api client to mocked client which returns return_value"""

    def decorator(func: Any):
        async def wrapper(*args, **kwargs):
            api = API("token")
            api.http_client = MockedClient(return_value)
            return await func(*args, **kwargs, api=api)

        return wrapper

    return decorator
