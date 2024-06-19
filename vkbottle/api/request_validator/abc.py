from abc import ABC, abstractmethod


class ABCRequestValidator(ABC):
    """Abstract Request Validator class
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/api/request_validator
    """

    @abstractmethod
    async def validate(self, request: dict) -> dict:
        pass
