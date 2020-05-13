from vkbottle.utils import logger
from vkbottle.api.api.util.token import AbstractTokenGenerator
from .util.requester import request
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .error_handler.error_handler import VKErrorHandler


class Request:
    def __init__(
        self, token_generator: "AbstractTokenGenerator", error_handler: "VKErrorHandler"
    ):
        self.token_generator: "AbstractTokenGenerator" = token_generator
        self.error_handler: "VKErrorHandler" = error_handler
        self.throw_errors: bool = True

    async def __call__(
        self,
        method: str,
        params: dict,
        throw_errors: bool = None,
        response_model=None,
        raw_response: bool = False,
    ):
        response = await request(
            method,
            params,
            await self.token_generator.get_token(method=method, params=params),
            request_instance=self,
            error_handler=self.error_handler,
        )

        logger.debug("Response: {}", response)

        if not response_model or raw_response:
            return response["response"]
        return response_model(**response).response

    def __repr__(self):
        return f"<Request {self.token_generator.__class__.__qualname__} throw_errors={self.throw_errors}>"
