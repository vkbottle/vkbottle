from vkbottle import Bot

bot = Bot("token")


@bot.on.message_handler()
async def handle(_):
    return "Hello world!"


bot.run_polling()
