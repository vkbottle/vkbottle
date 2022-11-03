from abc import ABC, abstractmethod
from typing import List, Union


class ABCTokenGenerator(ABC):
    async def __aenter__(self):
        return await self.get_token()

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def get_token(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__}>"


Token = Union[str, List[str], ABCTokenGenerator]
