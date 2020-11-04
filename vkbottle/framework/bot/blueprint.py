from vkbottle.framework.abc_blueprint import ABCBlueprint
from vkbottle.framework.bot.labeler import BotLabeler
from vkbottle.framework.bot.bot import Bot
from vkbottle.api import ABCAPI, API
from vkbottle.polling import ABCPolling
from vkbottle.modules import logger
from vkbottle.dispatch import BotRouter
from typing import Optional, Union


class BotBlueprint(ABCBlueprint):
    def __init__(
        self,
        name: Optional[str] = None,
        labeler: Optional[BotLabeler] = None,
        router: Optional[BotRouter] = None,
    ):
        if name is not None:
            self.name = name

        self.labeler = labeler or BotLabeler()
        self.router: BotRouter = router or BotRouter()
        self.constructed = False

    def construct(self, api: ABCAPI, polling: ABCPolling) -> "BotBlueprint":
        self.api = api
        self.polling = polling
        self.constructed = True
        return self

    def load(self, framework: "Bot") -> "BotBlueprint":
        framework.labeler.load(self.labeler)  # type: ignore
        logger.debug(f"Blueprint {self.name!r} loaded")
        return self.construct(framework.api, framework.polling)

    @property
    def on(self) -> BotLabeler:
        return self.labeler
