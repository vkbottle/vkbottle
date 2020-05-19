from vkbottle.user import User, Message
from vkbottle.api.token import LimitedTokenGenerator
from vkbottle.types.user_longpoll.events import FriendOnline
from vkbottle.rule import AbstractRule
import os
import time
import random
import typing

token_1 = os.environ["token_1"]
token_2 = os.environ["token_2"]
token_3 = os.environ["token_3"]
token_4 = os.environ["token_4"]

# Use ConsistentTokenGenerator if you are confident about the load of your polling
# LimitedTokenGenerator is the best choice to find out the problem of limit error at the start
generator = LimitedTokenGenerator([token_1, token_2, token_3, token_4])

user = User(token_1)
user.api.token_generator = generator


class Friend(AbstractRule):
    def __init__(self, user_ids: typing.Iterable[int]):
        self.user_ids = user_ids

    async def check(self, update: FriendOnline) -> bool:
        if abs(update.user_id) in self.user_ids:
            return True


@user.on.message_handler(text=["/time", "/время"], from_me=True)
async def new_message(ans: Message):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    return f"Текущее время: {current_time}"


@user.on.message_handler(
    text=[
        "/вероятность того что <thing",
        "/вероятность что <thing",
        "/вероятность <thing>",
    ]
)
async def probability(ans: Message, thing: str):
    await ans(
        f"Вероятность того, что {thing} равна {round(random.uniform(0.0, 1.0) * 100, 2)}%"
    )


@user.on.event.friend_online(Friend([1, 3]))
async def friend_online(event: FriendOnline):
    await user.api.messages.send(event.user_id, message="тест юзер лп, ты онлайн")


user.run_polling()
