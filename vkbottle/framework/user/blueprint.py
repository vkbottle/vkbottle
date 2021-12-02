from typing import TYPE_CHECKING, Optional, Union

from vkbottle.dispatch import Router
from vkbottle.framework.abc_blueprint import ABCBlueprint
from vkbottle.framework.labeler import UserLabeler
from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API
    from vkbottle.dispatch import ABCStateDispenser
    from vkbottle.framework.user.user import User
    from vkbottle.polling import ABCPolling


class UserBlueprint(ABCBlueprint):
    def __init__(
        self,
        name: Optional[str] = None,
        labeler: Optional[UserLabeler] = None,
        router: Optional[Router] = None,
    ):
        if name is not None:
            self.name = name

        self.labeler = labeler or UserLabeler()
        self.router: Router = router or Router()
        self.constructed = False

    def construct(
        self,
        api: Union["ABCAPI", "API"],
        polling: "ABCPolling",
        state_dispenser: "ABCStateDispenser",
    ) -> "UserBlueprint":
        self.api = api
        self.polling = polling
        self.state_dispenser = state_dispenser
        self.constructed = True
        return self

    def load(self, framework: "User") -> "UserBlueprint":
        framework.labeler.load(self.labeler)  # type: ignore
        logger.debug(f"Blueprint {self.name!r} loaded")
        return self.construct(framework.api, framework.polling, framework.state_dispenser)

    @property
    def on(self) -> UserLabeler:
        return self.labeler
