import typing
from abc import ABC, abstractmethod


class ABCRequestValidator(ABC):
    """ Abstract Response Validator class
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/low-level/api/response-validator.md
    """

    @abstractmethod
    async def validate(self, response: typing.Any) -> typing.Union[typing.Any, typing.NoReturn]:
        pass
