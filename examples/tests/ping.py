from vkbottle import Bot, Message
import os
from time import time

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])


@bot.on.message_handler(text=["/ping", "/"])
async def pronounce(ans: Message):
    return f"Пинг от вк: {round(time() - ans.date, 2)} сек"


bot.run_polling()
