from abc import ABC, abstractmethod
import typing


class Constructor(ABC):
    @abstractmethod
    def construct(self, *args, **kwargs) -> typing.ClassVar:
        """ Construct new object """
        pass
