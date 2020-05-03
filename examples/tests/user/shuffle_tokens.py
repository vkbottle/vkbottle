from vkbottle.user import User, Message
from vkbottle.api.token import LimitedTokenGenerator
import os

token_1 = os.environ["token_1"]
token_2 = os.environ["token_2"]
token_3 = os.environ["token_3"]
token_4 = os.environ["token_4"]

# Use ConsistentTokenGenerator if you are confident about the load of your polling
# LimitedTokenGenerator is the best choice to find out the problem of limit error at the start
generator = LimitedTokenGenerator([token_1, token_2, token_3, token_4])

user = User(token_1)
user.api.token_generator = generator


@user.on.message_handler()
async def new_message(ans: Message):
    if ans.from_id == user.user_id:
        await ans(ans.text)


user.run_polling()
