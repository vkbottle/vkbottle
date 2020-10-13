from vkbottle.bot import Bot, Message, run_multibot
from vkbottle.api import API
import logging

bot = Bot()
logging.basicConfig(level=logging.DEBUG)


@bot.on.message(lev="/инфо")  # LevensteinRule
async def info(message: Message):
    current_group = (await message.ctx_api.groups.get_by_id())[0]
    await message.answer(f"Название моей группы: {current_group.name}")


run_multibot(bot, apis=(API("token"), API("token2"), API("token3")))
