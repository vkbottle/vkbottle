from .abc import ABCResponseValidator
from vkbottle.exception_factory import VKAPIError
import typing


class VKAPIErrorResponseValidator(ABCResponseValidator):
    """ Default vk api error response validator
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/response-validator.md
    """

    async def validate(self, response: dict) -> typing.Union[typing.Any, typing.NoReturn]:
        if "error" not in response:
            return response
        raise VKAPIError(response["error"].get("error_code"), response["error"].get("error_msg"))
