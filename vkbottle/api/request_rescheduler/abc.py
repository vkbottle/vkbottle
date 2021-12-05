from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class ABCRequestRescheduler(ABC):
    @abstractmethod
    async def reschedule(
        self,
        ctx_api: Union["ABCAPI", "API"],
        method: str,
        data: dict,
        recent_response: Any,
    ) -> dict:
        pass
