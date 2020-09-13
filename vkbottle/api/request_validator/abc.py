from abc import ABC, abstractmethod
import typing


class ABCRequestValidator(ABC):
    """ Abstract Response Validator class
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/low-level/api/response-validator.md
    """

    @abstractmethod
    async def validate(self, response: typing.Any) -> typing.Union[typing.Any, typing.NoReturn]:
        pass
