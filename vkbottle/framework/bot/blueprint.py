import warnings
from typing import TYPE_CHECKING, Optional, Union

from typing_extensions import deprecated  # type: ignore

from vkbottle.dispatch import Router
from vkbottle.framework.abc_blueprint import ABCBlueprint
from vkbottle.framework.labeler import BotLabeler
from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API
    from vkbottle.dispatch import ABCStateDispenser
    from vkbottle.framework.bot import Bot
    from vkbottle.polling import ABCPolling


with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)

    @deprecated(
        "Blueprints was deprecated and will be removed in future releases, "
        "read about new code separation method in documentation: \n"
        "https://vkbottle.rtfd.io/ru/latest/tutorial/code-separation/",
        category=FutureWarning,
        stacklevel=0,
    )
    class BotBlueprint(ABCBlueprint):
        def __init__(
            self,
            name: Optional[str] = None,
            labeler: Optional[BotLabeler] = None,
            router: Optional[Router] = None,
        ):
            if name is not None:
                self.name = name

            self.labeler = labeler or BotLabeler()
            self.router: Router = router or Router()
            self.constructed = False

        def construct(
            self,
            api: Union["ABCAPI", "API"],
            polling: "ABCPolling",
            state_dispenser: "ABCStateDispenser",
        ) -> "BotBlueprint":
            self.api = api
            self.polling = polling
            self.state_dispenser = state_dispenser
            self.constructed = True
            return self

        def load(self, framework: "Bot") -> "BotBlueprint":
            framework.labeler.load(self.labeler)  # type: ignore
            logger.debug("Blueprint {!r} loaded", self.name)
            return self.construct(framework.api, framework.polling, framework.state_dispenser)

        @property
        def on(self) -> BotLabeler:
            return self.labeler
