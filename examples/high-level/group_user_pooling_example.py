from typing import Optional

from vkbottle_types.events.enums import UserEventType

from vkbottle import Bot
from vkbottle.framework.labeler import UserLabeler
from vkbottle.modules import logger
from vkbottle.polling.user_polling import UserPolling


class BotMessagesPooling(UserPolling):
    """The bot uses the User Long Poll to get its events.
    For example, such events can be exiting or entering a conversation.
    """

    def __init__(
        self,
        api: Optional["ABCAPI"] = None,
        group_id: Optional[int] = None,
        wait: Optional[int] = None,
        mode: Optional[int] = None,
        rps_delay: Optional[int] = None,
        error_handler: Optional["ABCErrorHandler"] = None,
    ):
        super().__init__(api, wait, mode, rps_delay, error_handler)
        self.group_id = group_id

    async def get_server(self) -> dict:
        logger.debug("Getting polling server...")
        if self.group_id is None:
            self.group_id = (await self.api.request("groups.getById", {}))["response"][0]["id"]
        return (await self.api.request("messages.getLongPollServer", {}))["response"]


token = "..."
bot = Bot(token, labeler=UserLabeler(), polling=BotMessagesPooling())


@bot.on.raw_event(UserEventType.CHAT_INFO_EDIT)
async def process_event(event):
    if event.object[1] == 7:
        type_action = "left"
    elif event.object[1] == 6:
        type_action = "returned to the"
    if event.object[1] in (6, 7):
        logger.info(
            "User {} {} conversation {}.",
            event.object[3],
            type_action,
            event.object[2]
        )


if __name__ == "__main__":
    bot.run_forever()
