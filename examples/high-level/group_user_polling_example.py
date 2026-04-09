import os
from typing import TYPE_CHECKING, Any

from vkbottle_types.events.enums import UserEventType
from vkbottle_types.events.user_events import RawUserEvent

from vkbottle import Bot
from vkbottle.framework.labeler import UserLabeler
from vkbottle.modules import logger
from vkbottle.polling.user_polling import UserPolling

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class BotMessagesPolling(UserPolling):
    """The bot uses the User Long Poll to get its events.
    For example, such events can be exiting or entering a conversation.
    """

    def __init__(
        self,
        api: "ABCAPI | None" = None,
        user_id: int | None = None,
        wait: int | None = None,
        mode: int | None = None,
        rps_delay: int | None = None,
        error_handler: "ABCErrorHandler | None" = None,
        group_id: int | None = None,
    ) -> None:
        super().__init__(
            api=api,
            user_id=user_id,
            wait=wait,
            mode=mode,
            rps_delay=rps_delay,
            error_handler=error_handler,
        )
        self.group_id = group_id

    async def get_server(self) -> dict[str, Any]:
        logger.debug("Getting polling server...")
        if self.group_id is None:
            self.group_id = (await self.api.request("groups.getById", {}))["response"]["groups"][
                0
            ]["id"]
        return (await self.api.request("messages.getLongPollServer", {}))["response"]


# Load token from system environment variable
# https://12factor.net/config
token = os.environ["TOKEN"]
bot = Bot(token, labeler=UserLabeler(), polling=BotMessagesPolling())

CHAT_LEFT = 7
CHAT_JOIN = 6


@bot.on.raw_event(UserEventType.CHAT_INFO_EDIT, dataclass=RawUserEvent)  # type: ignore
async def process_event(event):
    if event.object[1] not in (CHAT_JOIN, CHAT_LEFT):
        return
    type_action = "left" if event.object[1] == CHAT_LEFT else "returned to the"
    logger.info("User {} {} conversation {}.", event.object[3], type_action, event.object[2])


bot.run_forever()
