from vkbottle import Bot, Message, PhotoUploader, DocUploader
import os

# Add variable TOKEN to your env variables
bot = Bot(os.environ["TOKEN"])

photo_uploader = PhotoUploader(bot.api, generate_attachment_strings=True)
doc_uploader = DocUploader(bot.api, generate_attachment_strings=True)


@bot.on.message_handler(commands="картинка")
async def picture(ans: Message):
    photo = await photo_uploader.upload_message_photo("vkbottle_bot/data/1.jpg")
    await ans("Вот картинка:", attachment=photo)


@bot.on.message_handler(commands="документ")
async def document(ans: Message):
    doc = await doc_uploader.upload_doc_to_message(
        "vkbottle_bot/data/2.txt", ans.peer_id
    )
    await ans("Вот документ:", attachment=doc)


@bot.on.message_handler(text="по ссылке <link>")
async def from_link(ans: Message, link: str):
    data = await photo_uploader.get_data_from_link(link)
    await ans(
        "А вот и оно!", attachment=await photo_uploader.upload_message_photo(data)
    )


bot.run_polling()
