from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text
from typing import Optional
import logging
import random
import os

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


bot.run_forever()
