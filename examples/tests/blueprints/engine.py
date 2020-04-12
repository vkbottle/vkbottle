from vkbottle import Bot, Message
from .plugins import fare_bp, greet_bp
import os

bot = Bot(tokens=os.environ["TOKEN"], debug="DEBUG")
bot.set_blueprints(fare_bp, greet_bp)


@bot.on.message_handler(text="Where are the blueprints?")
async def wrapper(ans: Message):
    await ans("They’re on top!")


bot.run_polling(skip_updates=True)