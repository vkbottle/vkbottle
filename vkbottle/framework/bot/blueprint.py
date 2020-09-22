from vkbottle.framework.abc_blueprint import ABCBlueprint
from vkbottle.framework.bot.labeler import BotLabeler
from vkbottle.framework.bot.bot import Bot
from vkbottle.api import ABCAPI
from vkbottle.polling import ABCPolling
from vkbottle.dispatch import BotRouter
from typing import Optional


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
        framework.router.middlewares.extend(self.router.middlewares)
        framework.router.error_handler.error_handlers.update(  # type: ignore
            self.router.error_handler.error_handlers
        )
        framework.labeler.load(self.labeler)  # type: ignore
        return self.construct(framework.api, framework.polling)

    @property
    def on(self) -> BotLabeler:
        return self.labeler
