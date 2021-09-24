from abc import ABC, abstractmethod
from typing import Any, NewType, Optional

HTTPMiddlewareResponse = NewType("HTTPMiddlewareResponse", bool)


class ABCHTTPMiddleware(ABC):
    """Abstract class for http-client middleware
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/http/http-middleware.md
    """

    @abstractmethod
    async def pre(
        self, method: str, url: str, data: Optional[dict] = None, **kwargs
    ) -> Optional[HTTPMiddlewareResponse]:
        pass

    @abstractmethod
    async def post(self, response: Any):
        pass
