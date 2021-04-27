import typing

from vkbottle.exception_factory import VKAPIError

from .abc import ABCResponseValidator

if typing.TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class VKAPIErrorResponseValidator(ABCResponseValidator):
    """ Default vk api error response validator
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/low-level/api/response-validator.md
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

        code, msg = response["error"].get("error_code"), response["error"].get("error_msg")

        if ctx_api.ignore_errors:
            return None

        raise VKAPIError(code, msg, response)
