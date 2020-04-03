from vkbottle.user import User
from vkbottle.user.types import Message
from vkbottle.rule import VBMLUserRule

token_1 = "..."
token_2 = "..."
token_3 = "..."

user = User([token_1, token_2, token_3])


@user.on.message_new(VBMLUserRule("hi, <name>"))
async def wrapper(ans: Message, name):
    await ans(f"I'm not a {name}!")


user.run_polling()
