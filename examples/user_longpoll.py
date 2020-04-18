from vkbottle.user import User, Message

token_1 = "..."
token_2 = "..."
token_3 = "..."

user = User([token_1, token_2, token_3])


@user.on.message_handler(text="hi, <name>")
async def wrapper(ans: Message, name: str):
    await ans(f"I'm not a {name}!")


user.run_polling()
