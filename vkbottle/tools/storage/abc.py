from abc import ABC, abstractmethod
from typing import Any, Hashable


class ABCStorage(ABC):
    """Abstract storage class
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/tools/storage.md
    """

    @abstractmethod
    def get(self, key: Hashable) -> Any:
        pass

    @abstractmethod
    def set(self, key: Hashable, value: Any) -> None:
        pass

    @abstractmethod
    def delete(self, key: Hashable) -> None:
        pass

    @abstractmethod
    def contains(self, key: Hashable) -> bool:
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __contains__(self, item: str) -> bool:
        return self.contains(item)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.set(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        return self.get(key)
