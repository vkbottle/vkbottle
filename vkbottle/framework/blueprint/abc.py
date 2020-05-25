from vkbottle.framework.framework.branch import ABCBranchGenerator, DictBranch
from vkbottle.framework.framework.handler import MiddlewareExecutor
from vkbottle.api.api.api import Api
from vkbottle.api.api.error_handler import (
    VKErrorHandler,
    DefaultErrorHandler,
)
from abc import ABCMeta, abstractmethod
import typing


class AbstractBlueprint(metaclass=ABCMeta):
    _name: typing.Optional[str] = None
    _description: typing.Optional[str] = None

    @abstractmethod
    def __init__(self, name: str = None, description: str = None) -> None:
        self.branch: typing.Optional[ABCBranchGenerator] = DictBranch()
        self.middleware: MiddlewareExecutor = MiddlewareExecutor()
        self.error_handler: VKErrorHandler = DefaultErrorHandler()

        self.api: Api = None
        self._name = name or "Unknown"
        self._description = description or "Unknown"

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
