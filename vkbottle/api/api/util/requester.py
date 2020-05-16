from vkbottle.const import API_VERSION, API_URL
from vkbottle.utils.exceptions import VKError
from vkbottle.api.api.category import Categories
from vkbottle.http import HTTPRequest
from vkbottle.utils import logger, to_snake_case, from_attr

import time
import asyncio
import typing

if typing.TYPE_CHECKING:
    from ..error_handler import VKErrorHandler


async def request(
    method: str,
    params: dict,
    token: str,
    session: HTTPRequest = None,
    error_handler: "VKErrorHandler" = None,
    request_instance=None,
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
                [method.split(".")[0], to_snake_case(method.split(".")[1])]
                if "." in method
                else method,
                (request_instance, None),
            ),
            params,
            raw_error=response["error"],
        )
        if not error_handler:
            raise exception
        return await error_handler.handle_error(exception)
    return response
