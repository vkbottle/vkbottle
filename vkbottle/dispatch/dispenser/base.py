from enum import Enum
from typing import Any, ClassVar

from vkbottle.modules import pydantic


class BaseStateGroup(str, Enum):
    __slots__ = ()

    def __str__(self) -> str:
        return get_state_repr(self)


def get_state_repr(state: BaseStateGroup) -> str:
    return f"{state.__class__.__name__}:{state.value}"


class StateRepresentation(str):
    __slots__ = ()

    def __eq__(self, __x: object) -> bool:
        if isinstance(__x, BaseStateGroup):
            return self == get_state_repr(__x)
        return super().__eq__(__x)


class StatePeer(pydantic.BaseModel):
    peer_id: int
    state: str
    payload: ClassVar[dict] = {}

    @pydantic.validator("state", pre=True)
    def validate_state(cls, v: Any) -> str:
        if isinstance(v, BaseStateGroup):
            return StateRepresentation(v)
        elif isinstance(v, str):
            return v
        msg = f"State value must be `string` or `BaseStateGroup`, got `{type(v)}`"
        raise ValueError(msg)
