from vkbottle.const import API_VERSION, API_URL
from vkbottle.utils.exceptions import VKError
from vkbottle.api.api.category import Categories
from vkbottle.http import HTTPRequest
from vkbottle.utils import logger, to_snake_case, from_attr
from vkbottle.api.api.util.token import AbstractTokenGenerator

import time
import typing
import asyncio


async def request(
    method: str,
    params: dict,
    token: str,
    throw_errors: bool = True,
    session: HTTPRequest = None,
    request_instance: typing.Optional["Request"] = None,
):
    url = "{}{method}/?access_token={token}&v={version}".format(
        API_URL, method=method, token=token, version=API_VERSION,
    )

    session = session or HTTPRequest()
    response = await session.post(url, data=params or {})

    if not isinstance(response, dict):
        delay = 1

        while not isinstance(response, dict):
            logger.error(
                "\n---"
                f"{time.strftime('%m-%d %H:%M:%S', time.localtime())} - DELAY {delay * 5} sec\n"
                f"Check your internet connection. Maybe VK died, request returned: {response}"
                f"Error appeared after request: {method}"
            )
            await asyncio.sleep(delay * 5)
            response = await session.post(url, data=params or {})

        logger.success(
            f"--- {time.strftime('%m-%d %H:%M:%S', time.localtime())}\n"
            f"- METHOD SUCCESS after {5 * sum(range(1, delay))} sec\n"
            f"RESPONSE: {response}\n"
        )

    if "error" in response:
        logger.debug(
            "Error after request {method}, response: {r}", method=method, r=response
        )
        exception = VKError(
            response["error"]["error_code"],
            response["error"]["error_msg"],
            from_attr(
                Categories,
                [method.split(".")[0], to_snake_case(method.split(".")[1])],
                (request_instance, None),
            ),
            params,
            raw_error=response["error"],
        )
        if throw_errors:
            raise exception

        logger.debug(f"Error ignored {exception}")
    return response


class Request:
    def __init__(self, token_generator: AbstractTokenGenerator):
        self.token_generator: AbstractTokenGenerator = token_generator
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
            throw_errors=throw_errors
            if throw_errors is not None
            else self.throw_errors,
            request_instance=self,
        )

        logger.debug("Response: {}", response)

        if not response_model or raw_response:
            return response["response"]
        return response_model(**response).response

    def __repr__(self):
        return f"<Request {self.token_generator.__class__.__qualname__} throw_errors={self.throw_errors}>"
