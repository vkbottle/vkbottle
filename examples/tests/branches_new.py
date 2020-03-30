from vkbottle import Bot, Message
from vkbottle.rule import VBMLRule
from vkbottle.branch import ClsBranch, ExitBranch, rule_disposal, Branch
import os


# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])


class LovelessBranch(ClsBranch):
    async def branch(self, ans: Message, *args):
        return "I don't love you forever"


@bot.branch.simple_branch(branch_name="nun")
async def branch_wrapper(ans: Message, word):
    if ans.text.lower() in ["exit", "stop"]:
        await ans("As you want to!")
        return ExitBranch()
    await ans(word)


@bot.branch.cls_branch(branch_name="another")
class AnotherBranch(ClsBranch):
    @rule_disposal(VBMLRule("what <some>"))
    async def some(self, ans: Message, some):
        self.context["s"] = some
        await ans(f"I don't know what {some} is that")
        return ExitBranch()

    async def branch(self, ans: Message, *args):
        return f"Saying {self.context['word']}"

    async def exit(self, ans: Message):
        await ans(self.context)
        await ans("is this the escape?")


@bot.on.message_handler(text=["say <word>", "add <word>"])
async def pronounce(ans: Message, word):
    bot.branch.add(ans.peer_id, "another", word=word)
    return "Okay!"


@bot.on.message_handler(text="love")
async def loveless(ans: Message):
    await ans("Loveless..")
    return Branch(LovelessBranch)

bot.branch.add_branch(LovelessBranch)
bot.run_polling()
