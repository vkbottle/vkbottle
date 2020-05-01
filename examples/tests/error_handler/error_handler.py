from vkbottle.framework import swear
from vkbottle.bot import Bot, Message
from vkbottle import VKError
import os


# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"], debug=True)

async def exc_kick(e: BaseException, ans: Message):
    await ans("Не могу кикнуть! Ошибка " + str(e))

@bot.on.chat_message(commands=["самобан", "selfban"])
@swear(VKError, exception_handler=exc_kick)
async def hi(ans: Message):
    await bot.api.messages.remove_chat_user(ans.chat_id, ans.from_id)
    return "Ура кикнул"

bot.run_polling()
