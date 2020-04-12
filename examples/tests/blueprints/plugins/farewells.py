from vkbottle import Blueprint, Message

bp = Blueprint(name="Farewells")


@bp.on.message_handler(text="Goodbye!")
async def farewell_wrapper(ans: Message):
    await ans("Bye, nice to meet you.")


@bp.on.message_handler(text="Sorry, I gotta go")
async def leaving(ans: Message):
    await ans("Bet, see you later.")


@bp.on.message_handler(text="New description <text>")
async def set_description(ans: Message, text: str):
    bp.description(text)
    await ans("The description of the blueprint has changed!")