import typing, asyncio, types
import inspect

from .cls import FunctionBranch, AbstractBranch

from ...utils import logger
from ...api.exceptions import BranchError
from ...framework.rule import AbstractMessageRule

BRANCH_DATA = ".BRANCHES.txt"


class CoroutineBranch(AbstractBranch):
    coroutine: typing.Callable = None

    async def enter(self, ans):
        logger.info("Branch {} entered at", self.key or self.coroutine.__name__)

    async def exit(self, ans):
        logger.info("Branch {} exit at", self.key or self.coroutine.__name__)

    async def branch(self, ans):
        return await self.coroutine(ans)


class BranchManager:
    def __init__(self, plugin_folder: str):
        self._meet_up: typing.Dict[str, AbstractBranch] = {}
        self._branch_queue: typing.Dict[int, AbstractBranch] = {}

    def simple_branch(self, branch_name: str = None):
        def decorator(func: typing.Callable):
            if not asyncio.iscoroutinefunction(func):
                raise BranchError("Branch functions should be async")
            self._meet_up[branch_name or func.__name__] = FunctionBranch(
                branch_name or func.__name__, call=func
            )
            return func

        return decorator

    def add_branch(self, branch: typing.Callable, name: str = None):
        if inspect.isclass(type(branch)):
            self._meet_up[name or branch.__name__] = branch(name)
        elif asyncio.iscoroutinefunction(branch):
            self._meet_up[name or branch.__name__] = FunctionBranch(
                name or branch.__name__, call=branch
            )
        else:
            raise BranchError("Branch Callable should be an AbstractBranch (ClsBranch) or a async function")

    def cls_branch(self, branch_name: str = None):
        def decorator(cls: typing.ClassVar):
            self._meet_up[branch_name or cls.__name__] = cls(branch_name)
            return cls

        return decorator

    @property
    def queue(self) -> typing.Dict[int, AbstractBranch]:
        return self._branch_queue

    @property
    def branches(self) -> typing.Dict[str, AbstractBranch]:
        return self._meet_up

    def add(
        self,
        uid: int,
        branch: typing.Union[typing.Callable, str, AbstractBranch],
        **context
    ) -> None:
        if isinstance(branch, str):
            if branch not in self._meet_up:
                raise BranchError(
                    "Branch {} hasn't been yet assigned with decorator".format(branch)
                )
            state = CoroutineBranch(branch)
            state.coroutine = self._meet_up[branch]
        elif isinstance(branch, typing.Coroutine):
            q = {b.data["call"]: b for b in self._meet_up.values() if "call" in b.data}
            if branch not in q:
                raise BranchError(
                    "Branch {} hasn't been yet assigned with decorator".format(
                        branch.__name__
                    )
                )
            state = CoroutineBranch(q[branch])
            state.coroutine = branch
        else:
            for k, v in self._meet_up.items():
                if isinstance(v, branch):
                    branch = self._meet_up[k]
                    break
        branch.create(**context)
        self._branch_queue[uid] = branch

    async def load(
        self, uid: int
    ) -> typing.Tuple[
        typing.Dict[
            str,
            typing.Union[
                typing.Tuple[
                    typing.Callable, typing.List[AbstractMessageRule], typing.Callable
                ]
            ],
        ],
        AbstractBranch,
    ]:
        if uid in self._branch_queue:
            branch = self._branch_queue.get(uid)
            disposal = dict(
                inspect.getmembers(branch, predicate=lambda obj: isinstance(obj, tuple))
            )
            disposal["default"] = [branch.__class__.branch, []]
            return disposal, branch

    def exit(self, uid: int) -> AbstractBranch:
        if uid in self._branch_queue:
            return self._branch_queue.pop(uid, None)
