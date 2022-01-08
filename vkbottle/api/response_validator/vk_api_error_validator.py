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
            if "response" not in response:
                # invalid response, just igrnore it
                return response
            elif not (
                (
                    isinstance(response.get("response"), list)
                    and any(item.get("error") for item in response["response"])
                )
            ):
                # response is not a list of errors
                return response

        if ctx_api.ignore_errors:
            return None
        if isinstance(response.get("response"), list):
            # find first error in list
            error = next(item["error"] for item in response["response"] if item.get("error"))
        else:
            error = response["error"]
        # list of errors has a special error object with description and code instead of error_msg and error_code
        code = error.pop("error_code") if "error_code" in error else error.pop("code")
        if error.get("description"):
            error["error_msg"] = error.pop("description")
            error["request_params"] = [{"key": key, "value": value} for key, value in data.items()]
        exception = SPECIFIC_ERRORS.get(code, VKAPIError[code])

        if exception == CaptchaError and getattr(ctx_api, "captcha_handler"):
            key = await ctx_api.captcha_handler(exception(**error))  # type: ignore
            return await ctx_api.request(
                method,
                {**data, "captcha_sid": error["captcha_sid"], "captcha_key": key},
            )

        raise exception(**error)
