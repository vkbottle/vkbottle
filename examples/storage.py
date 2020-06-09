from vkbottle import Bot, Message
from vkbottle.framework import CtxStorage
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])
bot.extension.storage.set("written", 0)


@bot.on.message_handler()
async def any_message(ans: Message):
    storage = CtxStorage()
    messages_written = storage.get("written") + 1
    storage.set("written", messages_written)
    await ans(f"Ого мне написали уже {messages_written}")


bot.run_polling()
