from abc import ABC, abstractmethod
from typing import Any


class ABCRequestValidator(ABC):
    """Abstract Request Validator class
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/api/request_validator
    """

    @abstractmethod
    async def validate(self, request: dict[str, Any]) -> dict[str, Any]:
        pass


__all__ = ("ABCRequestValidator",)
