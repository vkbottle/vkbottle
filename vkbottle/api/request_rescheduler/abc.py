from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class ABCRequestRescheduler(ABC):
    @abstractmethod
    async def reschedule(
        self,
        ctx_api: typing.Union["ABCAPI", "API"],
        method: str,
        data: dict,
        recent_response: typing.Any,
    ) -> dict:
        pass
