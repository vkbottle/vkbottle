from enum import Enum

import pydantic
import typing_extensions as typing


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


if not typing.TYPE_CHECKING:
    State = typing.Union[str, StateRepresentation]
else:
    State: typing.TypeAlias = str


class StatePeer(pydantic.BaseModel):
    peer_id: int
    state: State
    payload: dict[str, typing.Any] = pydantic.Field(default_factory=dict[str, typing.Any])

    model_config = pydantic.ConfigDict(frozen=True, arbitrary_types_allowed=True, strict=True)

    @pydantic.field_validator("state", mode="before")
    def validate_state(cls, v: typing.Any) -> str:
        if isinstance(v, BaseStateGroup):
            return StateRepresentation(v)
        elif isinstance(v, str):
            return v
        msg = f"State value must be `string` or `BaseStateGroup`, got `{type(v)}`"
        raise ValueError(msg)
