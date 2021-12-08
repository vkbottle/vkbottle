from typing import TYPE_CHECKING, Any, Dict, NoReturn, Type, Union

from vkbottle.exception_factory import CaptchaError, VKAPIError

from .abc import ABCResponseValidator

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


SPECIFIC_ERRORS: Dict[int, Type[VKAPIError]] = {14: CaptchaError}


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
            return response

        if ctx_api.ignore_errors:
            return None

        error = response["error"]
        code = error.pop("error_code")

        exception = SPECIFIC_ERRORS.get(code, VKAPIError[code])

        if exception == CaptchaError and getattr(ctx_api, "captcha_handler"):
            key = await ctx_api.captcha_handler(exception(**error))  # type: ignore
            return await ctx_api.request(
                method, {**data, "captcha_sid": error["captcha_sid"], "captcha_key": key}
            )

        raise exception(**error)
