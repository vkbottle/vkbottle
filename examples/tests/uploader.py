from vkbottle import Bot, Message, PhotoUploader, DocUploader
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])

photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True)
doc_uploader = DocUploader(bot.api, generate_attachment_strings=True)


@bot.on.message_handler(commands="картинка")
async def picture(ans: Message):
    photo = await photo_uploader.upload_message_photo("vkbottle_bot/img/1.jpg")
    await ans("Вот картинка:", attachment=photo)


@bot.on.message_handler(commands="документ")
async def document(ans: Message):
    doc = await doc_uploader.upload_doc_to_message(
        "vkbottle_bot/img/2.txt", ans.peer_id
    )
    await ans("Вот документ:", attachment=doc)


bot.run_polling()
