import os

from vkbottle.bot import Bot, Message
from vkbottle.tools import DocMessagesUploader, PhotoMessageUploader

bot = Bot(os.environ["token"])
doc_uploader = DocMessagesUploader(bot.api)
photo_uploader = PhotoMessageUploader(bot.api)


# already uploaded picture
@bot.on.message(command="ларс")
async def lars_handler(m: Message):
    await m.answer(attachment="photo-41629685_457239401")


# on-handler processing upload
@bot.on.message(command="ридми")
async def readme_handler(m: Message):
    doc = await doc_uploader.upload(
        file_source="../../README.md",
        peer_id=m.peer_id,
    )
    await m.answer(attachment=doc)


@bot.on.message(command="лого")
async def logo_handler(m: Message):
    photo = await photo_uploader.upload("../../docs/logo.png", m.peer_id)
    await m.answer(attachment=photo)


bot.run_forever()
