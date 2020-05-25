from abc import ABC, abstractmethod
from vkbottle.utils import ContextInstanceMixin
from .storage import ABCStorage
import typing


class FromExtension:
    def __init__(self, attribute: str):
        self.attribute = attribute


class AbstractExtension(ABC, ContextInstanceMixin):
    def __init__(self):
        pass

    @abstractmethod
    def random_id(self) -> int:
        pass

    @property
    @abstractmethod
    def storage(self) -> ABCStorage:
        pass

    @abstractmethod
    def api_instance(self):
        pass

    @abstractmethod
    def group_id(self) -> int:
        pass

    def __repr__(self):
        return f"<Extension {self.__class__.__qualname__}>"


def dispatch(value: typing.Any) -> typing.Any:
    if isinstance(value, FromExtension):
        return getattr(AbstractExtension.get_current(), value.attribute)()
    return value
