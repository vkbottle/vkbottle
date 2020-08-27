from .abc import ABCResponseValidator
from vkbottle.exception_factory import VKBottleError
from vkbottle.modules import json
import typing


class JSONValidator(ABCResponseValidator):
    """ Default response json-parse validator
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/response-validator.md
    """

    async def validate(
        self, response: typing.Union[str, dict]
    ) -> typing.Union[typing.Any, typing.NoReturn]:
        if isinstance(response, dict):
            return response
        elif isinstance(response, str):
            return json.loads(response)

        raise VKBottleError("VK didn't returned anything")
