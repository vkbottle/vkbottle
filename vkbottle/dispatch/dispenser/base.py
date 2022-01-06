from enum import Enum
from typing import Union

from pydantic import BaseModel, validator


class BaseStateGroup(Enum):
    pass


def get_state_repr(state: BaseStateGroup) -> str:
    return f"{state.__class__.__name__}:{state.value}"


class StatePeer(BaseModel):
    peer_id: int
    state: str
    payload: dict = {}

    @validator("state", pre=True)
    def validate_state(cls, v: Union[BaseStateGroup, str]) -> str:
        if isinstance(v, BaseStateGroup):
            return get_state_repr(v)
        elif isinstance(v, str):
            return v
        raise ValueError(f"State value must be `string` or `BaseStateGroup`, got `{type(v)}`")
