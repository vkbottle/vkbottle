# Uploaders

Загрузка медиа разного типа в вк

Существует несколько типов аплоадеров:

* audio - загрузка аудио
* doc - загрузка документов разного типа
* photo - загрузка фото
* speech - загрузка аудиофайлов для распознавание речи
* video - загрузка видео

## Пример

```python
from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot

bot = Bot("token")
photo_uploader = PhotoMessageUploader(bot.api)


@bot.on.message(text="photo")
async def handler(message):
    photo = await photo_uploader.upload(
        file_source="photo.png",
        peer_id=m.peer_id,
    )
    await message.answer(attachment=photo)

bot.run_forever()
```

## Интерфейс аплоадера

Аплоадер принимает объект `API` при инициализации.

Аплоадеры имеет два метода:

* `.upload(...)`
* `.raw_upload(...)`

Оба метода имеют одинаковый интерфейс, но различаются в том, что первый метод возвращает готовую строку аттачмента, а второй - словарь с ответом сервера.
!!! warning "Внимание"
    Не все аплоадеры имеют метод `upload`, для них невозможно вернуть строку аттачмента

Все аплоадеры различаются методом получения сервера. Получить сервер аплоадера можно с помощью метода `.get_server(...)`

Так же у аплоадеров есть методы базового класса, одинаковые для всех:

* `.upload_files(url, files)` - загрузка файлов методом POST
* `.get_bytes_io(data)` - приводит сырые байты в подходящий для вк вид
* `.generate_attachment_string(attachment_type, owner_id, item_id, access_key)` - делает строку, которую вк принимает, как медиа для отправки
* `.read(file_source)` - читает файл, если file_source строка, a если байты - возвращает их

Обычно нужен только метод `upload`

## Виды аплоадеров

* Для фото
    * `PhotoMessageUploader` - загрузка в сообщение
    * `PhotoToAlbumUploader` - загрузка в альбом
    * `PhotoWallUploader` - загрузка на стену
    * `PhotoFaviconUploader` - загрузка аватарки
    * `PhotoChatFaviconUploader` - загрузка аватарки беседы
    * `PhotoMarketUploader` - загрузка картинки для товара

* Для документов
    * `DocWallUploader` - загрузка документов на стену
    * `DocMessagesUploader` - загрузка документов в сообщение
    * `VoiceMessageUploader` - загрузка голосовых сообщений
    * `GraffitiUploader` - загрузка граффити

* `AudioUploader` - загрузка аудио

* `VideoUploader` - загрузка видео

## Дополнительные примеры

* [Uploaders example](https://github.com/vkbottle/vkbottle/blob/master/examples/high-level/uploaders_example.py)
