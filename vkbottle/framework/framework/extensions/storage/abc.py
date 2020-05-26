from abc import ABC, abstractmethod
import typing


class ABCStorage(ABC):
    @abstractmethod
    def get(self, key: str) -> typing.Any:
        pass

    @abstractmethod
    def set(self, key: str, value: typing.Any) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def contains(self, key: str) -> bool:
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __contains__(self, item: str) -> bool:
        return self.contains(item)

    def __setitem__(self, key: str, value: typing.Any) -> None:
        self.set(key, value)

    def __getitem__(self, item: str) -> typing.Any:
        return self.get(item)
