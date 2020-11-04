from abc import ABC, abstractmethod
from vkbottle.api.request_rescheduler.abc import ABCRequestRescheduler
import typing

if typing.TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class ABCResponseValidator(ABC):
    """ Abstract Response Validator class
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/low-level/response-validator.md
    """

    @abstractmethod
    async def validate(
        self,
        method: str,
        data: dict,
        response: typing.Any,
        ctx_api: typing.Union["ABCAPI", "API"],
    ) -> typing.Union[typing.Any, typing.NoReturn]:
        pass
