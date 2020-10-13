from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.message(text=["привет<!>", "hi"])
async def hi_handler(message: Message):
    await message.answer("Привет!")


@bp.on.message(text="здравст<!>")
async def hello_handler(message: Message):
    await message.answer("Здравствуйте!")
