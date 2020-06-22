# Правила

Обработка всех хендлеров со стороны пользователя строится на правилах. Правило - это кусок кода который при исполнении показывает подходит ли событие под этот хендлер или нет

## Встроенные правила, col rules

Вы видите полный список встроенных правил ниже:

`commands` - команда с префиксом /  
`sticker` - сообщение содержит стикер с указанным ID  
`levenstein` или `lev` - сообщение проверяется по расстоянию левенштейна с исходным  
`payload` - проверяет что payload равен указанному  
`from_me` - для User LP, проверить что сообщение от текущего пользователя (True) или наоборот (False)

## Откуда брать правила?

Большой список правил [представлен здесь](https://github.com/timoniq/vkbottle/blob/master/vkbottle/framework/framework/rule/rule.py)

Если вам нужно что-то особенное приступайте к созданию своего правила

## Создание своего правила

Любое правило должно наследоваться от `AbstractRule` или `AbstractMessageRule` если для сообщений. Класс должен имплементировать асинхронную функцию `check` которая должна возвращать `True` в случае успеха:

```python
from vkbottle.rule import AbstractMessageRule
from vkbottle import Message

class MyHandsomeRule(AbstractMessageRule):
    async def check(self, message: Message) -> bool:
        photos = message.get_photo_attachments()
        if photos:
            self.context.args.append(photos)
            return True
```

<blockquote>Собственный init тоже можно заимплементировать</blockquote>

Что делает это правило:

Получает список фото-вложений с помощью [метода датакласса](https://github.com/timoniq/vkbottle/blob/40e634a291a262c5dedacd3fb5fa8d8bc26eac9d/vkbottle/types/objects/messages.py#L246)  
Если список не пустой добавляет в возвращаемые в хендлер аргументы этот список и обозначает что правило пройдено с помощью `return True`

<blockquote>Для того чтобы добавить позиционные аргументы в контекст используются <code>context.args</code>. Для непозиционных <code>context.kwargs</code></blockquote>

Теперь мы можем написать такой хендлер:

```python
@bot.on.message(MyHandsomeRule())
async def wrapper(ans: Message, photos): # no type only not to be misunderstood
    await ans.reply(f"Спасибо за эти {len(photos)} фотографий!")
```

Готово!