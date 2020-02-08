from vkbottle import Bot, Message
import os, random, string, asyncio
from asyncio import sleep

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"], debug=False)
STRINGS = []
TIMES = 0


def random_string(length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


async def stress(ans: Message):
    for s in STRINGS.copy():
        await ans(f"/r {s}")
        await sleep(0.3)
    await ans("/re - to see results")


@bot.on.message_handler(text=["/s", "/s <t:int>"])
async def pronounce(ans: Message, t=100):
    globals()["STRINGS"] = [random_string() for i in range(t)]
    globals()["TIMES"] = t
    bot.loop.create_task(stress(ans))


@bot.on.message_handler(text=["/results", "/re"])
async def res():
    return f"{TIMES - len(STRINGS)}/{TIMES}. I haven't seen {STRINGS}"


@bot.on.message_handler(text="/r <s>")
async def response(s):
    if s in STRINGS:
        STRINGS.pop(STRINGS.index(s))

bot.run_polling()
