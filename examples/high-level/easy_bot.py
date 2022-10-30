import logging
import os
import random
from typing import Optional

from vkbottle import GroupEventType, GroupTypes, Keyboard, Text, VKAPIError
from vkbottle.bot import Bot, Message
from vkbottle.modules import logger

bot = Bot(os.environ["token"])

# Logging level can be set through .basicConfig(level=LOGGING_LEVEL)
# but if you use loguru the instruction is different.
# ---
# If you use loguru you need to remove default logger and add new with
# level specified logging level, visit https://github.com/Delgan/loguru/issues/138
logging.basicConfig(level=logging.INFO)

# Documentation for keyboard builder > tools/keyboard
KEYBOARD = Keyboard(one_time=True).add(Text("Съесть еще", {"cmd": "eat"})).get_json()
EATABLE = ["мороженое", "макароны", "суп"]


# If you need to make handler respond for 2 different rule set you can
# use double decorator like here it is or use filters (OrRule here)
@bot.on.message(text=["/съесть <item>", "/съесть"])
@bot.on.message(payload={"cmd": "eat"})
async def eat_handler(message: Message, item: Optional[str] = None):
    if item is None:
        item = random.choice(EATABLE)
    await message.answer(f"Ты съел <<{item}>>!", keyboard=KEYBOARD)


# This need to be set to True if you want to use that rule
bot.labeler.message_view.replace_mention = True


# Will reply to message that exactly match bot mention
# eg "@bot" if mention=True or just starts with mention if mention=False
# Mention will be removed from message text and can be accessed via message.mention with id and text fields
@bot.on.message(mention=True)
async def mention_handler(message: Message):
    await message.reply("Привет, чего вы хотите?")


# You can use raw_event to handle any event type, the advantage is
# free dataclass, for example it can be dict if you have some problems
# with module types quality
@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:

        # Basic API call, please notice that bot.api is
        # not accessible in case multibot is used, API can be accessed from
        # event.ctx_api
        await bot.api.messages.send(
            peer_id=event.object.user_id, message="Спасибо за подписку!", random_id=0
        )

    # Read more about exception handling in documentation
    # low-level/exception_handling/exception_handling
    except VKAPIError[901]:
        logger.error("Can't send message to user with id {}", event.object.user_id)


# Runs loop > loop.run_forever() > with tasks created in loop_wrapper before,
# read the loop wrapper documentation to comprehend this > tools/loop-wrapper.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
