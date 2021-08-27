import typing

from vkbottle.exception_factory import CaptchaError, VKAPIError

from .abc import ABCResponseValidator

if typing.TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


SPECIFIC_ERRORS: typing.Dict[int, typing.Type[VKAPIError]] = {14: CaptchaError}


class VKAPIErrorResponseValidator(ABCResponseValidator):
    """Default vk api error response validator
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/response-validator.md
    """

    async def validate(
        self,
        method: str,
        data: dict,
        response: typing.Any,
        ctx_api: typing.Union["ABCAPI", "API"],
    ) -> typing.Union[typing.Any, typing.NoReturn]:
        if "error" not in response:
            return response

        if ctx_api.ignore_errors:
            return None

        error = response["error"]
        code = error["error_code"]

        exception = SPECIFIC_ERRORS.get(code, VKAPIError[code])
        raise exception(**error)
