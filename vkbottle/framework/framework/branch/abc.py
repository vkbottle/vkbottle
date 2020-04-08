import typing
from abc import ABC, abstractmethod
from .cls import AbstractBranch
from ..rule import AbstractMessageRule

Branch = typing.Union[str, AbstractBranch]
BranchRule = typing.Tuple[typing.Callable, typing.List[AbstractMessageRule]]


class AbstractBranchGenerator(ABC):
    Disposal = typing.Dict[str, BranchRule]
    cls_branch: typing.Any
    simple_branch: typing.Any

    @abstractmethod
    def from_function(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def add_branch(self, branch: AbstractBranch, name: str = None, **context) -> AbstractBranch:
        ...

    @property
    @abstractmethod
    async def queue(self) -> typing.List[int]:
        ...

    @abstractmethod
    async def add(self, uid: int, branch: Branch):
        ...

    @abstractmethod
    async def load(self, uid: int) -> typing.Tuple["AbstractBranchGenerator.Disposal", AbstractBranch]:
        ...

    @abstractmethod
    async def exit(self, uid: int):
        ...
