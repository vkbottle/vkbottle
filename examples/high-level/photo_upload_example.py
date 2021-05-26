import os

from vkbottle.bot import Bot, Message
from vkbottle.tools import DocMessagesUploader

bot = Bot(os.environ["token"])


# already uploaded picture
@bot.on.message(command="ларс")
async def lars_handler(m: Message):
    await m.answer(attachment="photo-41629685_457239401")


# on-handler processing upload
@bot.on.message(command="ридми")
async def readme_handler(m: Message):
    doc = await DocMessagesUploader(bot.api).upload(
        "readme.md", "../../README.md", peer_id=m.peer_id
    )
    await m.answer(attachment=doc)


bot.run_forever()
