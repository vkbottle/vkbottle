from vkbottle import Bot, Message, VKError
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"], debug="ERROR")


@bot.on.message_handler(text="/r <s>")
async def pronounce(s):
    return f"/r {s}"


bot.run_polling()
