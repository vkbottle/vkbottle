from abc import ABC, abstractmethod
from ..bot import AnyBot

class AbstractTemplate(ABC):
    def __init__(self, bot: AnyBot):
        self.bot: AnyBot = bot

    @abstractmethod
    def ready(self, *args, **kwargs) -> "AbstractTemplate":
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
