from typing import TYPE_CHECKING, Any, Union

from vkbottle.exception_factory import CaptchaError, VKAPIError
from vkbottle.modules import logger

from .abc import ABCResponseValidator

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class VKAPIErrorResponseValidator(ABCResponseValidator):
    """Default vk api error response validator
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/api/response-validator
    """

    async def validate(
        self,
        method: str,
        data: dict,
        response: Any,
        ctx_api: Union["ABCAPI", "API"],
    ) -> Any:
        if "error" not in response:
            if "response" not in response:
                request_params = [{"key": key, "value": value} for key, value in data.items()]
                raise VKAPIError[1](
                    error_msg=f"Unknown response from {method}: {response}",
                    request_params=request_params,
                )

            if isinstance(response["response"], list) and any(
                "error" in item for item in response["response"] if isinstance(item, dict)
            ):
                logger.info("API error(s) in response wasn't handled: {!r}", response["response"])

            return response

        if ctx_api.ignore_errors:
            return None
        error = response["error"]
        code = error.pop("error_code")

        if VKAPIError[code] is CaptchaError and ctx_api.captcha_handler is not None:
            key = await ctx_api.captcha_handler(CaptchaError(**error))  # type: ignore
            return await ctx_api.request(
                method,
                data={**data, "captcha_sid": error["captcha_sid"], "captcha_key": key},
            )

        raise VKAPIError[code](**error)
