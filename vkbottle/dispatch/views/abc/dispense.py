import typing
from abc import abstractmethod
from typing import Generic, Optional, TypeVar

from .view import ABCView

if typing.TYPE_CHECKING:
    from vkbottle.dispatch.handlers.abc import ABCHandler

T_contra = TypeVar("T_contra", list, dict, contravariant=True)
F_contra = TypeVar("F_contra", contravariant=True)


class ABCDispenseView(ABCView[T_contra], Generic[T_contra, F_contra]):
    handlers: typing.List["ABCHandler[F_contra]"]

    @abstractmethod
    def get_state_key(self, event: F_contra) -> Optional[int]:
        pass
