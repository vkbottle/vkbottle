from vkbottle import Bot, Message
from vkbottle.branch import ClsBranch, ExitBranch
import os


# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])


@bot.branch.simple_branch()
async def branch_wrapper(ans: Message, word):
    if ans.text.lower() in ["exit", "stop"]:
        await ans("As you want to!")
        return ExitBranch()
    await ans(word)


@bot.branch.cls_branch(branch_name="another")
class Branch(ClsBranch):
    async def branch(self, ans: Message):
        return "An another class branch"

    async def exit(self, ans: Message):
        await ans("life on mars?")


@bot.on.message_handler(text=["say <word>", "add <word>"])
async def pronounce(ans: Message, word):
    bot.branch.add(ans.peer_id, Branch, word=word)
    return "Okay!"

bot.run_polling()
