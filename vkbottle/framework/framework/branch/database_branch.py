import asyncio
import inspect
import typing
from abc import abstractmethod

from vkbottle.utils.exceptions import BranchError
from vkbottle.utils.json import json

from .abc import ABCBranchGenerator, AbstractBranch, Branch, GeneratorType
from .cls import ClsBranch, CoroutineBranch


class DatabaseBranch(ABCBranchGenerator):
    def __init__(self):
        self.names: typing.Dict[str, typing.Type[AbstractBranch]] = {}
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

    def get_branch(self, branch_name: str, context: typing.Union[str, dict]) -> Branch:
        bare = self.names[branch_name]
        if isinstance(bare, tuple):
            bare = bare[0]
        branch = bare()
        if isinstance(context, str):
            context = json.loads(context)
        branch.context = context
        branch.key = branch_name
        return branch

    def from_function(
        self, func: typing.Callable, branch_name: str = None,
    ) -> AbstractBranch:
        if not asyncio.iscoroutinefunction(func):
            raise BranchError("Branch functions should be async")

        from_function_branch = CoroutineBranch()
        from_function_branch.key = branch_name or func.__name__
        from_function_branch.data = {"call": func}

        return from_function_branch

    def add_branch(
        self, branch: typing.Type[ClsBranch], name: str = None, **context
    ) -> AbstractBranch:
        self.names[name or branch.__name__] = branch
        return branch

    @property
    async def queue(self) -> typing.List[int]:
        return await self.all_users()

    @property
    def branches(self) -> typing.Dict[str, AbstractBranch]:
        return self.names

    def add_branches(self, new_branches: typing.Dict[str, AbstractBranch]):
        self.names.update(new_branches)

    async def add(
        self,
        uid: int,
        branch: typing.Union[Branch, str],
        call_enter: bool = True,
        **context,
    ):
        if isinstance(branch, str):
            if branch not in self.names:
                raise BranchError(
                    f"Branch {branch!r} hasn't yet been assigned with decorator"
                )
        else:
            if branch not in self.names.values():
                raise BranchError(
                    f"Branch {branch.__name__!r} hasn't yet been assigned with decorator"
                )
            branch = dict((v, k) for k, v in self.names.items())[branch]

        dumped_context = context

        if self.__class__.generator in [GeneratorType.DATABASE, GeneratorType.ABSTRACT]:
            dumped_context = json.dumps(context)

        await self.set_user(uid, branch, dumped_context)

        if call_enter:
            await self.get_branch(branch, context).enter()

    async def load(
        self, uid: int
    ) -> typing.Tuple["ABCBranchGenerator.Disposal", AbstractBranch]:
        branch_name, context = await self.get_user(uid)
        branch = self.get_branch(branch_name, context)

        if not branch:
            raise BranchError(
                f"User {uid} is signed with undefined branch {branch_name!r}"
            )

        disposal = dict(
            inspect.getmembers(branch, predicate=lambda obj: isinstance(obj, tuple))
        )
        disposal["default"] = [branch.__class__.branch, []]
        return disposal, branch

    async def exit(self, uid: int, call_exit: bool = True):
        if uid in await self.queue:
            if call_exit:
                name, context = await self.get_user(uid)
                branch = self.get_branch(name, context)
                await branch.exit()
            await self.delete_user(uid)

    def get_current(self, *args, **kwargs) -> "DatabaseBranch":
        return self
