import typing
from abc import ABC, abstractmethod


class ABCStorage(ABC):
    """ Abstract storage class
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/tools/storage.md
    """

    @abstractmethod
    def get(self, key: typing.Hashable) -> typing.Any:
        pass

    @abstractmethod
    def set(self, key: typing.Hashable, value: typing.Any) -> None:
        pass

    @abstractmethod
    def delete(self, key: typing.Hashable) -> None:
        pass

    @abstractmethod
    def contains(self, key: typing.Hashable) -> bool:
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __contains__(self, item: str) -> bool:
        return self.contains(item)

    def __setitem__(self, key: typing.Hashable, value: typing.Any) -> None:
        self.set(key, value)

    def __getitem__(self, key: typing.Hashable) -> typing.Any:
        return self.get(key)
