from abc import ABC, abstractmethod
from vkbottle.exception_factory import VKAPIError
from typing import Callable, Awaitable, Union, Iterable, NoReturn, Any


class ABCAPIErrorHandler(ABC):
    ErrorHandler = Callable[[VKAPIError, dict], Awaitable]  # type: ignore

    @abstractmethod
    async def handle_error(self, code: int, description: str, data: dict):
        pass

    @abstractmethod
    def register_api_error_handler(self, code: int, error_handler: ErrorHandler) -> NoReturn:
        pass

    def api_error_handler(self, code: Union[int, Iterable[int]]) -> Any:
        if isinstance(code, int):
            code = [code]

        def decorator(
            handler: "ABCAPIErrorHandler.ErrorHandler",
        ) -> "ABCAPIErrorHandler.ErrorHandler":
            for c in code:  # type: ignore
                self.register_api_error_handler(c, handler)
            return handler

        return decorator
