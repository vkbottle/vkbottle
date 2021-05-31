from abc import abstractmethod
from typing import Any, Optional

from .abc import ABCView


class ABCDispenseView(ABCView):
    @abstractmethod
    def get_state_key(self, event: Any) -> Optional[int]:
        pass
