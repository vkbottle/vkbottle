from .abc import ABCResponseValidator
import typing


class GetResponseValidator(ABCResponseValidator):
    """ Default get response validator
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/response-validator.md
    """

    async def validate(self, response: dict) -> typing.Union[typing.Any, typing.NoReturn]:
        return response.get("response")
