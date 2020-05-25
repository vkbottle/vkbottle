import enum
import typing
from abc import ABC, abstractmethod

from vkbottle.framework.framework.branch.standard_branch import BranchCheckupKey
from vkbottle.utils.util import ContextInstanceMixin
from .cls import AbstractBranch
from ..rule import AbstractMessageRule

Branch = typing.Union[str, AbstractBranch]
BranchRule = typing.Tuple[typing.Callable, typing.List[AbstractMessageRule]]


class GeneratorType(enum.Enum):
    ABSTRACT = "abstract"
    DATABASE = "database"
    DICT = "dict"


class ABCBranchGenerator(ABC, ContextInstanceMixin):
    Disposal = typing.Dict[str, BranchRule]
    cls_branch: typing.Any
    simple_branch: typing.Any
    generator: GeneratorType = GeneratorType.ABSTRACT
    checkup_key: BranchCheckupKey = BranchCheckupKey.PEER_ID

    @abstractmethod
    def from_function(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def add_branch(self, branch: AbstractBranch, name: str = None) -> AbstractBranch:
        ...

    @property
    @abstractmethod
    async def queue(self) -> typing.List[int]:
        ...

    @property
    @abstractmethod
    def branches(self) -> typing.Dict[str, typing.Tuple[AbstractBranch, ...]]:
        ...

    @abstractmethod
    def add_branches(
        self, new_branches: typing.Dict[str, typing.Tuple[AbstractBranch, ...]]
    ):
        ...

    @abstractmethod
    async def add(self, uid: int, branch: Branch, **context):
        ...

    @abstractmethod
    async def load(
        self, uid: int
    ) -> typing.Tuple["ABCBranchGenerator.Disposal", AbstractBranch]:
        ...

    @abstractmethod
    async def exit(self, uid: int):
        ...

    def __repr__(self):
        return f"<BranchGenerator {self.__class__.__name__}>"

    def __dict__(self):
        return self.branches
