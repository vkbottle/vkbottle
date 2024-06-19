import os

from vkbottle.bot import Bot, Message, rules
from vkbottle.tools import WaiterMachine

bot = Bot(os.environ["TOKEN"])
wm = WaiterMachine()


@bot.on.message(text="/wm")
async def greeting(message: Message):
    await message.answer("Как тебя зовут?")
    m, _ = await wm.wait(bot.on.message_view, message)
    await message.answer(f"Привет, {m.text.capitalize()}! Будем знакомы.")


@bot.on.message(text="/expiring")
async def expiring(message: Message):
    await message.answer("Напиши палиндром, быстро!")
    await wm.wait(
        bot.on.message_view,
        message,
        rules.FuncRule(lambda m: m.text == m.text[::-1]),
        default="Это не палиндром, думай быстрее!",
        expiration=10,
    )
    await message.answer("Отличный палиндром!")


bot.run_forever()
