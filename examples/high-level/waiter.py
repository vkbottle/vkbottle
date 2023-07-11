import os

from vkbottle.bot import Bot, Message
from vkbottle.tools import WaiterMachine

bot = Bot(os.environ["TOKEN"])
wm = WaiterMachine()


@bot.on.message(text="/wm")
async def greeting(message: Message):
    await message.answer("Как тебя зовут?")
    m, _ = await wm.wait(bot.on.message_view, message)
    await message.answer(f"Привет, {m.text.capitalize()}! Будем знакомы.")


bot.run_forever()
