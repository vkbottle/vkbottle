from abc import ABC, abstractmethod
from typing import NoReturn, Union


class ABCRequestValidator(ABC):
    """Abstract Request Validator class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/request_validator.md
    """

    @abstractmethod
    async def validate(self, request: dict) -> Union[dict, NoReturn]:
        pass
