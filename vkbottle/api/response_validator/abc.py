from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class ABCResponseValidator(ABC):
    """Abstract Response Validator class
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/api/response-validator
    """

    @abstractmethod
    async def validate(
        self,
        method: str,
        data: dict,
        response: Any,
        ctx_api: Union["ABCAPI", "API"],
    ) -> Any:
        pass
