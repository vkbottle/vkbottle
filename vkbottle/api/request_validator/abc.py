from abc import ABC, abstractmethod
from typing import Any, NoReturn, Union


class ABCRequestValidator(ABC):
    """Abstract Response Validator class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/response-validator.md
    """

    @abstractmethod
    async def validate(self, response: Any) -> Union[Any, NoReturn]:
        pass
