from time import time as current

from tortoise import Tortoise

from vkbottle import Bot, Message
from vkbottle.ext import Middleware
from vkbottle.rule import AbstractMessageRule
from .tortoise_models import User

bot = Bot("token")

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
    async def pre(self, message: Message, *args):
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


bot.run_polling(skip_updates=False, on_startup=init_db)
