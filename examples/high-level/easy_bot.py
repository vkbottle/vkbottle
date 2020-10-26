import logging
import os
import random
from typing import Optional

from vkbottle import Keyboard, Text, GroupTypes, GroupEventType, VKAPIError
from vkbottle.bot import Bot, Message

bot = Bot(os.environ["token"])
logging.basicConfig(level=logging.INFO)

EATABLE = ["мороженое", "диван", "штаны", "пальто", "код"]
KEYBOARD = Keyboard(one_time=True).add(Text("Съесть еще", {"cmd": "eat"})).get_json()


@bot.on.message(text=["/съесть <item>", "/съесть"])
@bot.on.message(payload={"cmd": "eat"})
async def eat_handler(message: Message, item: Optional[str] = None):
    if item is None:
        item = random.choice(EATABLE)
    await message.answer(f"Ты съел <<{item}>>!", keyboard=KEYBOARD)


@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id, message="Спасибо за подписку!", random_id=0
        )
    except VKAPIError(901):
        pass


bot.run_forever()
