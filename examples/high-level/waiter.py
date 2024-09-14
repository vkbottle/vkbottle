import os

from vkbottle.bot import Bot, Message
from vkbottle.dispatch.handlers import MessageReplyHandler
from vkbottle.dispatch.rules.base import FuncRule, TextRule
from vkbottle.tools import WaiterMachine

bot = Bot(os.environ["TOKEN"])
wm = WaiterMachine()


@bot.on.message(text="/wm")
async def greeting(message: Message):
    await message.answer("Как тебя зовут?")
    m, _ = await wm.wait(
        bot.on.message_view,
        message,
        exit=MessageReplyHandler("Хорошо!", TextRule("/exit"), as_reply=True),
    )
    await message.answer(f"Привет, {m.text.capitalize()}! Будем знакомы.")


@bot.on.message(text="/expiring")
async def expiring(message: Message):
    await message.answer("Напиши палиндром, у тебя 10 секунд!")
    await wm.wait(
        bot.on.message_view,
        message,
        FuncRule(lambda m: m.text == m.text[::-1]),
        default=MessageReplyHandler("Это не палиндром, думай быстрее!", as_reply=True),
        expiration=10,
    )
    await message.answer("Отличный палиндром!")


bot.run_forever()
