from abc import ABCMeta, abstractmethod
import typing


class AbstractBlueprint(metaclass=ABCMeta):
    _name: typing.Optional[str] = None
    _description: typing.Optional[str] = None

    @abstractmethod
    def __init__(self, name: str = None, description: str = None) -> None:
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description: str):
        self._description = new_description

    def __repr__(self):
        return f"<Blueprint {self.__class__.__qualname__} name={self.name} description={self.description}>"
