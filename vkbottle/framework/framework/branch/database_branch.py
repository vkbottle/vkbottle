from abc import abstractmethod
from .abc import AbstractBranchGenerator, Branch, AbstractBranch, GeneratorType
from .standart_branch import ImmutableBranchData
from .cls import CoroutineBranch
from vkbottle.api.exceptions import BranchError
from vkbottle.utils.json import json
import typing
import asyncio
import inspect


class DatabaseBranch(AbstractBranchGenerator):
    def __init__(self):
        self.names: typing.Dict[str, typing.Type[AbstractBranch]] = {}
        self.encoding: str = "utf-8"
        self.generator = GeneratorType.DATABASE

    @abstractmethod
    async def get_user(self, uid: int) -> typing.Tuple[str, typing.Union[str, dict]]:
        pass

    @abstractmethod
    async def set_user(self, uid: int, branch: str, context: str) -> None:
        pass

    @abstractmethod
    async def delete_user(self, uid: int):
        pass

    @abstractmethod
    async def all_users(self) -> typing.List[int]:
        pass

    async def from_function(
        self, func: typing.Callable, branch_name: str = None,
    ) -> typing.Tuple[AbstractBranch, ImmutableBranchData]:
        if not asyncio.iscoroutinefunction(func):
            raise BranchError("Branch functions should be async")

        class FromFunctionDatabaseBranch(CoroutineBranch):
            key = branch_name or func.__name__
            data = {"call": func}

        return FromFunctionDatabaseBranch

    def add_branch(
        self, branch: AbstractBranch, name: str = None, **context
    ) -> AbstractBranch:
        self.names[name or branch.__name__] = branch
        return branch

    @property
    async def queue(self) -> typing.List[int]:
        return await self.all_users()

    @property
    async def branches(self) -> typing.Dict[str, AbstractBranch]:
        return self.names

    async def add(self, uid: int, branch: Branch, **context):
        if isinstance(branch, str):
            if branch not in self.names:
                raise BranchError(
                    f"Branch {branch} hasn't yet been assigned with decorator"
                )
        else:
            if branch not in self.names.values():
                raise BranchError(
                    f"Branch {branch.__name__} hasn't yet been assigned with decorator"
                )
            branch = dict((v, k) for k, v in self.names.items())[branch]
        await self.set_user(uid, branch, json.dumps(context).decode(self.encoding))

    async def load(
        self, uid: int
    ) -> typing.Tuple["AbstractBranchGenerator.Disposal", AbstractBranch]:
        branch_name, context = await self.get_user(uid)
        if isinstance(context, str):
            context = json.loads(context)
        branch = self.names.get(branch_name)()
        branch.context = context
        branch.key = branch_name
        if not branch:
            raise BranchError(
                f'User {uid} is signed with undefined branch "{branch_name}"'
            )

        disposal = dict(
            inspect.getmembers(branch, predicate=lambda obj: isinstance(obj, tuple))
        )
        disposal["default"] = [branch.__class__.branch, []]
        return disposal, branch

    async def exit(self, uid: int):
        if uid in await self.queue:
            await self.delete_user(uid)
