from vkbottle.user import User, types
from vkbottle.rule import VBMLUserRule, AbstractUserRule
from vkbottle import TaskManager
import os

user = User(os.environ["TOKEN"], debug="DEBUG")
user.mode(2)


class OnlyMe(AbstractUserRule):
    async def check(self, message: types.Message):
        if await message.from_id == user.user_id:
            return True


@user.on.message_new(VBMLUserRule("тест"), OnlyMe())
async def test(ans: types.Message):
    await ans("тест пройден")


tm = TaskManager(user.loop)
tm.add_task(user.run())
tm.run()
