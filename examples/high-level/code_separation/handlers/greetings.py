from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()


@labeler.message(text=["привет<!>", "hi"])
async def hi_handler(message: Message):
    await message.answer("Привет!")


@labeler.message(text="здравст<!>")
async def hello_handler(message: Message):
    await message.answer("Здравствуйте!")
