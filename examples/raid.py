from vkbottle import Bot, Message
from vkbottle.rule import VBMLRule
import vbml, asyncio

bot = Bot("token")


@bot.on.chat_message(VBMLRule(vbml.Pattern("/raid <text> <times:int>", lazy=False)))
async def raid(ans: Message, text: str, times: int):
    for i in range(times):
        await ans(text)
        await asyncio.sleep(0.2)


bot.run_polling()
