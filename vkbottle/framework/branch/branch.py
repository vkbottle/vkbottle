import typing, asyncio, types
import inspect

from .cls import CoroutineBranch, AbstractBranch
from .standart_branch import ImmutableBranchData

from ...utils import logger
from ...api.exceptions import BranchError
from ...framework.rule import AbstractMessageRule

BRANCH_DATA = ".BRANCHES.txt"


class BranchManager:
    def __init__(self):
        self._meet_up: typing.Dict[str, typing.Tuple[AbstractBranch, ImmutableBranchData]] = {}
        self._branch_queue: typing.Dict[int, typing.Tuple[AbstractBranch, ImmutableBranchData]] = {}

    def simple_branch(self, branch_name: str = None):
        def decorator(func: typing.Callable):
            if not asyncio.iscoroutinefunction(func):
                raise BranchError("Branch functions should be async")
            self._meet_up[branch_name or func.__name__] = (CoroutineBranch, ImmutableBranchData(
                branch_name or func.__name__, call=func
            ))
            return func
        return decorator

    def add_branch(self, branch: typing.Callable, name: str = None):
        if inspect.isclass(type(branch)):
            self._meet_up[name or branch.__name__] = (branch, ImmutableBranchData(name))
        elif asyncio.iscoroutinefunction(branch):
            self._meet_up[name or branch.__name__] = (CoroutineBranch, ImmutableBranchData(
                name or branch.__name__, call=branch
            ))
        else:
            raise BranchError("Branch Callable should be an AbstractBranch (ClsBranch) or a async function")

    def cls_branch(self, branch_name: str = None):
        def decorator(cls: typing.ClassVar):
            self._meet_up[branch_name or cls.__name__] = (cls, ImmutableBranchData(branch_name))
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
        state, data = None, None
        if isinstance(branch, str):
            if branch not in self._meet_up:
                raise BranchError(
                    "Branch {} hasn't been yet assigned with decorator".format(branch)
                )
            state, data = self._meet_up[branch]
        elif isinstance(branch, typing.Coroutine):
            q = {b[1].data["call"]: b for b in self._meet_up.values() if "call" in b[1].data}
            if branch not in q:
                raise BranchError(
                    "Branch {} hasn't been yet assigned with decorator".format(
                        branch.__name__
                    )
                )
            state, data = q[branch]
        else:
            for k, v in self._meet_up.items():
                if v[0] is branch:
                    state, data = self._meet_up[k]
                    break
        assert state and data, BranchError("Branch not found, maybe it still hasn't been assigned")
        branch = state(**data())
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
            del self._branch_queue[uid]
