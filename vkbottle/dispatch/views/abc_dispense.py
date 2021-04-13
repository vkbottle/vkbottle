from abc import abstractmethod
from .abc import ABCView
from typing import Optional


class ABCDispenseView(ABCView):
    @abstractmethod
    def get_state_key(self, event: dict) -> Optional[int]:
        pass
