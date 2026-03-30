import logging

from vkbottle.api import API
from vkbottle.bot import Bot, Message, run_multibot

# API for bot used in multibot is not required and may be
# forbidden later to avoid user-side mistakes with it's usage
# TIP: to access api in multibot handlers api should be
# requested from event.ctx_api
bot = Bot()
logging.basicConfig(level=logging.DEBUG)


@bot.on.message(lev="/инфо")  # lev > custom_rule from LevenshteinRule
async def info(message: Message):
    groups = (await message.ctx_api.groups.get_by_id()).groups
    if groups:
        await message.answer(f"Название моей группы: {groups[0].name}")


# Read more about multibot in documentation
# high-level/bot/multibot
run_multibot(bot, apis=(API("token"), API("token2"), API("token3")))
