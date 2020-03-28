from time import time as current

from tortoise import Tortoise

from vkbottle import Bot, Message, TaskManager
from vkbottle.rule import AbstractMessageRule
from vkbottle.ext import Middleware
from .tortoise_models import User

bot = Bot("token")
tm = TaskManager(bot.loop)

"""
Better works with tortoise.
Choose only asynchronous libraries to integrate them with vkbottle
"""


class Registered(AbstractMessageRule):
    async def check(self, message: Message):
        self.context.args.append(await User.get(uid=message.from_id))
        return True


@bot.middleware.middleware_handler()
class Register(Middleware):
    async def middleware(self, message: Message):
        if not await User.get_or_none(uid=message.from_id):
            await User.create(uid=message.from_id, time=current())
            await message("You are now registered")


@bot.on.message(Registered(), lev=["hi", "hello"])
async def wrapper(ans: Message, user: User):
    await ans(f"hi, my lil friend, unix time of registration: {user.time}")


async def init_db():
    await Tortoise.init(
        db_url="sqlite://users.db", modules={"models": ["tortoise_models"]}
    )
    await Tortoise.generate_schemas()


tm.add_task(bot.run(skip_updates=True))
tm.add_task(init_db())
tm.run()
