import typing
from abc import abstractmethod

from vkbottle.dispatch.rules import ABCRule


class ABCFilter(ABCRule):
    @property
    @abstractmethod
    def rules(self) -> typing.Iterable[ABCRule]:
        pass
