from vkbottle.const import API_VERSION, API_URL
from vkbottle.api.exceptions import VKError
from vkbottle.http import HTTPRequest
from vkbottle.utils import logger
import time
import asyncio


async def request(
    method: str,
    params: dict,
    token: str,
    throw_errors: bool = True,
    session: HTTPRequest = None,
    raw_response: bool = False,
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
            logger.critical(
                "\n---"
                f"{time.localtime()} - DELAY {delay * 5} sec\n"
                f"Check your internet connection. Maybe VK died, request returned: {response}"
                f"Error appeared after request: {method}",
            )
            await asyncio.sleep(delay * 5)
            delay += 1
            response = await session.post(url, data=params or {})

            logger.critical(
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

    if raw_response:
        return response
    return response["response"]


class Request:
    def __init__(self, token: str):
        self.token = token

    async def __call__(
        self,
        method: str,
        params: dict,
        throw_errors: bool = True,
        response_model=None,
        raw_response: bool = False,
    ):
        response = await request(
            method,
            params,
            self.token,
            throw_errors=throw_errors,
            raw_response=raw_response,
        )
        print(method, response)
        if not response_model:
            return response
        return response_model(**response)
