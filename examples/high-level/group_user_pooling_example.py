from typing import TYPE_CHECKING, Optional

from vkbottle_types.events.enums import UserEventType
from vkbottle_types.events.user_events import RawUserEvent

from vkbottle import Bot
from vkbottle.framework.labeler import UserLabeler
from vkbottle.modules import logger
from vkbottle.polling.user_polling import UserPolling

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI
    from vkbottle.exception_factory import ABCErrorHandler


class BotMessagesPooling(UserPolling):
    """The bot uses the User Long Poll to get its events.
    For example, such events can be exiting or entering a conversation.
    """

    def __init__(
        self,
        api: Optional["ABCAPI"] = None,
        user_id: Optional[int] = None,
        wait: Optional[int] = None,
        mode: Optional[int] = None,
        rps_delay: Optional[int] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
        group_id: Optional[int] = None,
    ):
        super().__init__(
            api=api,
            user_id=user_id,
            wait=wait,
            mode=mode,
            rps_delay=rps_delay,
            error_handler=error_handler,
        )
        self.group_id = group_id

    async def get_server(self) -> dict:
        logger.debug("Getting polling server...")
        if self.group_id is None:
            self.group_id = (await self.api.request("groups.getById", {}))["response"][0]["id"]
        return (await self.api.request("messages.getLongPollServer", {}))["response"]


token = "..."
bot = Bot(token, labeler=UserLabeler(), polling=BotMessagesPooling())


@bot.on.raw_event(UserEventType.CHAT_INFO_EDIT, dataclass=RawUserEvent)  # type: ignore
async def process_event(event):
    type_action = "left" if event.object[1] == 7 else "returned to the"
    if event.object[1] in (6, 7):
        logger.info("User {} {} conversation {}.", event.object[3], type_action, event.object[2])


bot.run_forever()
