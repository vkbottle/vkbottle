from typing import Optional, Union

from vkbottle.api import ABCAPI, API
from vkbottle.dispatch import ABCStateDispenser, BotRouter
from vkbottle.framework.abc_blueprint import ABCBlueprint
from vkbottle.framework.bot.bot import Bot
from vkbottle.framework.bot.labeler import BotLabeler
from vkbottle.modules import logger
from vkbottle.polling import ABCPolling


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

    def construct(
        self, api: Union[ABCAPI, API], polling: ABCPolling, state_dispenser: ABCStateDispenser
    ) -> "BotBlueprint":
        self.api = api
        self.polling = polling
        self.state_dispenser = state_dispenser
        self.constructed = True
        return self

    def load(self, framework: "Bot") -> "BotBlueprint":
        framework.labeler.load(self.labeler)  # type: ignore
        logger.debug(f"Blueprint {self.name!r} loaded")
        return self.construct(framework.api, framework.polling, framework.state_dispenser)

    @property
    def on(self) -> BotLabeler:
        return self.labeler
