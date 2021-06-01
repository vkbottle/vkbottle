from abc import abstractmethod
from typing import TYPE_CHECKING, Optional

from .view import ABCView

if TYPE_CHECKING:
    from vkbottle_types.events import Event


class ABCDispenseView(ABCView):
    @abstractmethod
    def get_state_key(self, event: "Event") -> Optional[int]:
        pass
