from vkbottle.user import User, types
from vkbottle.api.api.builtin import ConsistentTokenGenerator
import os

user = User()
user.api.token_generator = ConsistentTokenGenerator(os.environ["token"].split())


@user.on.message_new()
async def deleter(message: types.Message):
    user.api.throw_errors = False
    await user.api.messages.delete(message.from_id, delete_for_all=True)
