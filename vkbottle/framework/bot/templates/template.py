from abc import ABC, abstractmethod
from ..bot import AnyBot, Bot
import typing


class AbstractTemplate(ABC):
    def __init__(self, bot: typing.Union[AnyBot, str], **kwargs):
        if isinstance(bot, str):
            bot = Bot(bot, **kwargs)
        self.bot: AnyBot = bot

    @abstractmethod
    def ready(self, *args, **kwargs) -> "AbstractTemplate":
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
