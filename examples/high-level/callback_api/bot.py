import os

from vkbottle import Bot
from vkbottle.bot import Message
from vkbottle.callback import BotCallback

# Load token from system environment variable
# https://12factor.net/config
TOKEN = os.environ["TOKEN"]
callback = BotCallback(url="http://example.com/whateveryouwant", title="my server")
bot = Bot(token=TOKEN, callback=callback)


@bot.on.message(text="привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(user_ids=[message.from_id])
    await message.answer(f"Hello, {users_info[0].first_name}")
