from vkbottle.bot import Blueprint, Message

bp = Blueprint(name="greetings", description="It was created to welcome users")


@bp.on.message_handler(text="Hello!")
async def hello_wrapper(ans: Message):
    await ans("Hello, how are you?")


@bp.on.message_handler(text="How are you doing?")
async def asking(ans: Message):
    await ans("I'm good and you?")
