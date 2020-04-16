from vkbottle.const import API_VERSION, API_URL
from vkbottle.api.exceptions import VKError
from vkbottle.http import HTTPRequest
from vkbottle.utils import logger
from .token import AbstractTokenGenerator

import time
import asyncio


async def request(
    method: str,
    params: dict,
    token: str,
    throw_errors: bool = True,
    session: HTTPRequest = None,
):
    url = "{}{method}/?access_token={token}&v={version}".format(
        API_URL, method=method, token=token, version=API_VERSION,
    )

    session = session or HTTPRequest()
    response = await session.post(url, data=params or {})

    if not isinstance(response, dict):
        while not isinstance(response, dict):
            # Works only on python 3.6+
            delay = 1
            logger.error(
                "\n---"
                f"{time.strftime('%m-%d %H:%M:%S', time.localtime())} - DELAY {delay * 5} sec\n"
                f"Check your internet connection. Maybe VK died, request returned: {response}"
                f"Error appeared after request: {method}",
            )
            await asyncio.sleep(delay * 5)
            delay += 1
            response = await session.post(url, data=params or {})

            logger.success(
                f"--- {time.strftime('%m-%d %H:%M:%S', time.localtime())}\n"
                f"- METHOD SUCCESS after {5 * sum(range(1, delay))} sec\n"
                f"RESPONSE: {response}\n",
            )

    if "error" in response:
        logger.debug(
            "Error after request {method}, response: {r}", method=method, r=response
        )
        if throw_errors:
            raise VKError(
                [response["error"]["error_code"], response["error"]["error_msg"]]
            )
        return response
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
            await self.token_generator.get_token(),
            throw_errors=throw_errors
            if throw_errors is not None
            else self.throw_errors,
        )

        logger.debug("Response: {}", response)

        if not response_model:
            return response["response"]
        resp = response_model(**response)
        if raw_response:
            return resp
        return resp.response

    def __repr__(self):
        return f"<Request {self.token_generator.__class__.__qualname__} throw_errors={self.throw_errors}>"
