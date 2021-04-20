from typing import Optional, Union

from vkbottle.api import ABCAPI, API
from vkbottle.dispatch import ABCStateDispenser, UserRouter
from vkbottle.framework.abc_blueprint import ABCBlueprint
from vkbottle.framework.user.user import User
from vkbottle.framework.user.labeler import UserLabeler
from vkbottle.modules import logger
from vkbottle.polling import ABCPolling


class UserBlueprint(ABCBlueprint):
    def __init__(
        self,
        name: Optional[str] = None,
        labeler: Optional[UserLabeler] = None,
        router: Optional[UserRouter] = None,
    ):
        if name is not None:
            self.name = name

        self.labeler = labeler or UserLabeler()
        self.router: UserRouter = router or UserRouter()
        self.constructed = False

    def construct(
        self, api: Union[ABCAPI, API], polling: ABCPolling, state_dispenser: ABCStateDispenser
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
