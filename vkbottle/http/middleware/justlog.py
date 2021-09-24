from typing import Any, Optional

from vkbottle.modules import logger

from .abc import ABCHTTPMiddleware


class JustLogHTTPMiddleware(ABCHTTPMiddleware):
    async def pre(self, method: str, url: str, data: Optional[dict] = None, **kwargs):
        logger.debug(
            f"{method.upper()} Request to {url}; data={data} "
            + "; ".join(f"{k}={v}" for k, v in kwargs.items())
        )

    async def post(self, response: Any):
        logger.debug(f"Response: {response}")
