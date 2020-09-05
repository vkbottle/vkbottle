from abc import ABC, abstractmethod
from .views import ABCView
from .middlewares import BaseMiddleware
from typing import List, Dict


class ABCRouter(ABC):
    views: Dict[str, "ABCView"]
    middlewares: List["BaseMiddleware"]

    @abstractmethod
    async def route(self, event: dict):
        pass
