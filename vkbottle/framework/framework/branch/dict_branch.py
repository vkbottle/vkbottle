import typing

from .abc import GeneratorType
from .database_branch import DatabaseBranch
from .standard_branch import ImmutableBranchData


class DictBranch(DatabaseBranch):
    user_states: typing.Dict[int, typing.Tuple[str, ...]] = {}
    generator = GeneratorType.DICT

    async def get_user(self, uid: int) -> typing.Tuple[str, typing.Union[str, dict]]:
        return self.user_states[uid]

    async def set_user(self, uid: int, branch: str, context: str) -> None:
        self.user_states[uid] = (branch, context)

    async def delete_user(self, uid: int):
        del self.user_states[uid]

    async def all_users(self) -> typing.List[int]:
        return list(self.user_states)

    def cls_branch(
        self, branch_name: str = None,
    ):
        def decorator(cls: typing.ClassVar):
            self.names[branch_name or cls.__name__] = (
                cls,
                ImmutableBranchData(branch_name),
            )
            return cls

        return decorator

    def simple_branch(self, branch_name: str = None):
        def decorator(func: typing.Callable):
            self.names[branch_name or func.__name__] = self.from_function(
                func, branch_name
            )
            return func

        return decorator
