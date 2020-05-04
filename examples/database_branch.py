import os

from tortoise import Tortoise  # my humble choice

from vkbottle import Bot, Message
from vkbottle.branch import ClsBranch, rule_disposal
from vkbottle.framework.framework.branch.database_branch import DatabaseBranch
from vkbottle.rule import VBMLRule
from examples.tortoise_models import UserState

"""
Database branch manager itself
"""


class SqliteBranch(DatabaseBranch):
    async def get_user(self, uid: int):
        """This method should return a tuple of two strings: branch name of the user and context"""
        user = await UserState.get(uid=uid)
        return user.branch, user.context

    async def set_user(self, uid: int, branch: str, context: str):
        """This method should make user's state or update it if exists"""
        user = await UserState.get_or_none(uid=uid)
        if user is not None:
            user.branch = branch
            user.context = context
            return await user.save()
        await UserState.create(uid=uid, branch=branch, context=context)

    async def all_users(self):
        """This method should return user_ids of all stated users"""
        return [user.uid async for user in UserState.all()]

    async def delete_user(self, uid: int):
        """This method should delete the user's instance from the database"""
        user = await UserState.get(uid=uid)
        await user.delete()


bot = Bot(os.environ["token"])
bot.branch = SqliteBranch()


class StoredBranch(ClsBranch):
    @rule_disposal(VBMLRule("/говорить <word>"))
    async def say(self, ans: Message, word: str):
        self.context["word"] = word
        return f"Теперь я буду говорить слово: {word}"

    @rule_disposal(VBMLRule("/остановить"))
    async def stop(self, ans: Message):
        await bot.branch.exit(ans.peer_id)
        return "Бранч остановлен!"

    async def branch(self, ans: Message, *args):
        if "word" not in self.context:
            return "Напиши /говорить <слово> чтобы оно сохранилось у меня в контексте!"
        user = await bot.api.users.get(ans.from_id)
        return f"{user[0].first_name}, твое слово: {self.context['word']}"


@bot.on.message_handler(commands=["start"])
async def start(ans: Message):
    await bot.branch.add(ans.peer_id, "talker")
    return "Ты в бранче!"


async def init_db():
    await Tortoise.init(
        db_url="sqlite://users.db", modules={"models": ["examples.tortoise_models"]}
    )
    await Tortoise.generate_schemas()


bot.branch.add_branch(StoredBranch, "talker")
bot.run_polling(on_startup=init_db)
