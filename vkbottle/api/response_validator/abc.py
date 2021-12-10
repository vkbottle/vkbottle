from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, NoReturn, Union

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class ABCResponseValidator(ABC):
    """Abstract Response Validator class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/api/response-validator.md
    """

    @abstractmethod
    async def validate(
        self,
        method: str,
        data: dict,
        response: Any,
        ctx_api: Union["ABCAPI", "API"],
    ) -> Union[Any, NoReturn]:
        pass
