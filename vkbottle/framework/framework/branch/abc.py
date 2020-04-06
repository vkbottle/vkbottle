import typing
from abc import ABC, abstractmethod
from .cls import AbstractBranch
from ..rule import AbstractMessageRule

Branch = typing.Union[str, AbstractBranch]
BranchRule = typing.Tuple[typing.Callable, typing.List[AbstractMessageRule]]
Disposal = typing.Tuple[typing.Dict[str, BranchRule]]


class AbstractBranchGenerator(ABC):
    def __init__(self):
        ...

    @abstractmethod
    def from_function(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def add_branch(self, branch: AbstractBranch, name: str) -> AbstractBranch:
        ...

    @property
    @abstractmethod
    def queue(self) -> typing.Dict[int, AbstractBranch]:
        ...

    @abstractmethod
    def add(self, uid: int, branch: Branch):
        ...

    @abstractmethod
    async def load(self, uid: int) -> typing.Tuple[Disposal]:
        ...

    @abstractmethod
    def exit(self, uid: int):
        ...
