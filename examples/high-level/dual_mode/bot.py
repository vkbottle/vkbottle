import os

from vkbottle import Bot
from vkbottle.bot import Message
from vkbottle.callback import BotCallback

# Load token from system environment variable
# https://12factor.net/config
TOKEN = os.environ["TOKEN"]
CALLBACK_URL = os.environ["CALLBACK_URL"]
CALLBACK_TITLE = os.getenv("CALLBACK_TITLE", "DualMode")

callback = BotCallback(url=CALLBACK_URL, title=CALLBACK_TITLE)
bot = Bot(token=TOKEN, callback=callback, dual_mode=True)


@bot.on.message(text="привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(user_ids=[message.from_id])
    await message.answer(f"Hello, {users_info[0].first_name}")
