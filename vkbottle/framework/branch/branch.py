import typing, asyncio

from .cls import FunctionBranch, AbstractBranch

from ...api.exceptions import BranchError

BRANCH_DATA = ".BRANCHES.txt"


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
            branch = self._meet_up[branch]
        elif isinstance(branch, typing.Coroutine):
            q = {b.data["call"]: b for b in self._meet_up.values() if "call" in b.data}
            if branch not in q:
                raise BranchError(
                    "Branch {} hasn't been yet assigned with decorator".format(
                        branch.__name__
                    )
                )
            branch = q[branch]
        else:
            for k, v in self._meet_up.items():
                if isinstance(v, branch):
                    branch = self._meet_up[k]
                    break
        branch.create(**context)
        self._branch_queue[uid] = branch

    def load(self, uid: int) -> AbstractBranch:
        if uid in self._branch_queue:
            return self._branch_queue.get(uid)

    def exit(self, uid: int) -> AbstractBranch:
        if uid in self._branch_queue:
            return self._branch_queue.pop(uid, None)
