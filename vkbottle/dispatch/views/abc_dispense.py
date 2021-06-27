from abc import abstractmethod
from typing import Optional

from .abc import ABCView


class ABCDispenseView(ABCView):
    @abstractmethod
    def get_state_key(self, event: dict) -> Optional[int]:
        pass
