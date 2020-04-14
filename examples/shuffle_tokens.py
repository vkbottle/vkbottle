from vkbottle.user import User, Message
from vkbottle.api.api.builtin import ConsistentTokenGenerator

token_1 = "..."
token_2 = "..."
token_3 = "..."
token_4 = "..."


generator = ConsistentTokenGenerator([token_1, token_2, token_3, token_4])

user = User(token_1)
user.api.token_generator = generator


@user.on.message_new()
async def new_message(ans: Message):
    if ans.from_id == user.user_id:
        await ans("Я что-то написал, да?")


user.run_polling()
