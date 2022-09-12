from typing import TYPE_CHECKING, Any, NoReturn, Union

from vkbottle.exception_factory import CaptchaError, VKAPIError
from vkbottle.modules import logger

from .abc import ABCResponseValidator

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class VKAPIErrorResponseValidator(ABCResponseValidator):
    """Default vk api error response validator
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/response-validator.md
    """

    async def validate(
        self,
        method: str,
        data: dict,
        response: Any,
        ctx_api: Union["ABCAPI", "API"],
    ) -> Union[Any, NoReturn]:
        if "error" not in response:
            if "response" not in response:
                # invalid response, just ignore it
                return response
            elif isinstance(response["response"], list):
                errors = [item["error"] for item in response["response"] if "error" in item]
                if errors:
                    logger.debug(
                        "{} API error(s) in response wasn't handled: {}", len(errors), errors
                    )
            return response

        if ctx_api.ignore_errors:
            return None
        error = response["error"]
        code = error.pop("error_code")

        if VKAPIError[code] is CaptchaError and ctx_api.captcha_handler:
            key = await ctx_api.captcha_handler(CaptchaError(**error))  # type: ignore
            return await ctx_api.request(
                method, {**data, "captcha_sid": error["captcha_sid"], "captcha_key": key}
            )

        raise VKAPIError[code](**error)
