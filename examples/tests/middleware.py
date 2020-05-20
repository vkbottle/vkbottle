from vkbottle import Bot, Message
from vkbottle.ext import Middleware
import os
from time import time

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"], debug="DEBUG")


@bot.middleware.middleware_handler()
class UserCheck(Middleware):
    async def pre(self, message: Message):
        if not message.from_id > 0:
            return False


@bot.on.message_handler(
    lev={"hello": ["reaction to hello"], "hi": {"source": "reaction to hi"}}
)
async def pronounce(ans: Message, source):
    return f"Hello! {source}"


bot.run_polling()
