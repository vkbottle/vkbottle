from vkbottle.user import User, Message
from vkbottle.api.token import ConsistentTokenGenerator
from vkbottle.rule import FromMe

token_1 = "..."
token_2 = "..."
token_3 = "..."
token_4 = "..."


generator = ConsistentTokenGenerator([token_1, token_2, token_3, token_4])

user = User(token_1)
user.api.token_generator = generator


@user.on.message_handler(FromMe())
async def new_message(ans: Message):
    await ans("Я что-то написал, да?")


user.run_polling()
