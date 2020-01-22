from vkbottle import Bot, Message
from vkbottle.framework.bot import Vals
from vbml import Patcher

bot = Bot("token", 1, debug=True, plugin_folder="examplebot")


class BottleValidators(Vals):
    def startswith(self, value: str, start: str):
        if value.startswith(start):
            return value


# Answer <Президент😎😎> to <!никнейм Ким-..>
@bot.on.message("!президент <name:startswith[Ким]>", lower=True)
async def wrapper(ans: Message, name):
    await ans(f"{name}😎😎")


bot.patcher.set_current(Patcher(validators=BottleValidators))
bot.run_polling()
