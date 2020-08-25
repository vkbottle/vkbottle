from abc import ABC, abstractmethod


class ABCAPI(ABC):
    """ Abstract API class
    Documentation: https://github.com/timoniq/vkbottle/tree/v3.0/docs/api/api.md
    """

    @abstractmethod
    async def request(self, method: str, data: dict) -> dict:
        pass
