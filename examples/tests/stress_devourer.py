from vkbottle import Bot, Message
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"], debug=False)


@bot.on.message_handler(text="/r <s>")
async def pronounce(s):
    return f"/r {s}"

bot.run_polling()
