from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API


class ABCRequestRescheduler(ABC):
    @abstractmethod
    async def reschedule(
        self,
        ctx_api: "ABCAPI | API",
        method: str,
        data: dict[str, Any],
        recent_response: Any,
    ) -> dict:
        pass
