## Использование API vk.com

Вы можете использовать API, которое предоставляет вконтакте прямо из коробки, не привязываясь к боту или юзеру. Либо же вы можете использовать его из бота или юзера.

### API
Используем чистое API:
```python
from vkbottle.api import API
tokens = ["token-1", "token-2"]
api = API(tokens=tokens, throw_errors=True)
```

| Параметр | Описание |
|--|--|
| tokens | список токенов / токен |
| generator | название генератора токенов (может быть переназначено позже) |
| throw_errors | нужно ли API Request выбрасывать исключение в случае неудачи |

**generator**  нужен при слишкой большой нагрузке (больше 20 запросов в секунду). Вы можете использовать такие генераторы:

| Название для поля `generator` | Класс из `vkbottle.api.api.builtin` | Описание |
|--|--|--|
| consistent | ConsistentTokenGenerator | В этом генераторе токены являются циклический очередью, токены используются последовательно с каждым запросом |
| random | RandomTokenGenerator | Токены выбираются рандомно из данного списка |
| limited | LimitedTokenGenerator | Токены используются максимальное возможное кол-во (`limit`) раз |
| classified (-) | ClassifiedTokenGenerator | Редко используемый генератор, доступен только через переопределение, нужен, если токены имеют разные права. Вместо списка токенов этот генератор получает схему (`vkbottle.api.api.schema`) (документация по schema тут) |

Хороший пример с генератором: [https://github.com/timoniq/vkbottle/tree/master/examples/tests/user/shuffle_tokens.py]()

  - **throw_errors** определяет стандартное поведение API
 . После,  он может быть переопределен только при вызове собственно метода

  - **tokens** - может быть как списком токенов,  так и одним токеном. В ботах рекомендуется использовать до 2
  токенов (максимальная нагрузка - 40 запросов в секунду), тогда как при работе с юзерами может понадобится больше 6 из-за невероятно низкого лимита (3 запроса в секунду)

  - **Дополнительно** Пример кастомного генератора:  

Напишем генератор для определения токена из двух типов по условию (vk me и обычный):

```python
from vkbottle.api.api.token import AbstractTokenGenerator
import typing
import random

class CustomTokenGenerator(AbstractTokenGenerator):
    def __init__(self, vk_me_tokens: typing.List[str], tokens: typing.List[str]):
        self.vk_me_tokens = vk_me_tokens
        self.tokens = tokens
    
    async def get_token(self, method: str, params: dict) -> str:
        if method in ["messages.setActivity", "messages.send"]:
            return random.choice(self.vk_me_tokens)
        return random.choice(self.tokens)
```

Теперь добавим его в наш API:

```python
from vkbottle.api import API

api = API()
api.token_generator = CustomTokenGenerator(["vkme-token"], ["token-1", "token-2"])
```

### Bot API, User API
Для вызова API методов с инициированным ботом потребуется использовать атрибут класса `Bot.api`:

```python
from vkbottle.bot import Bot
from vkbottle.user import User
from vkbottle.api.api.builtin import LimitedTokenGenerator

bot_token = "token-1"
user_tokens = ["user-token-1", "user-token-2", "user-token-3"]
user_generator = LimitedTokenGenerator(user_tokens, limit=3)

bot = Bot(tokens=bot_token, throw_errors=False)
user = User() # При переопределении генератора, токены оставлять не обязательно
user.api.token_generator = user_generator
# bot.api
```
### Обращение к методам

VKBottle поддерживает только асинхронный вызов методов (операторы **async/await**)

#### Вызов

Для обращения к API требуется написать группу и название метода:

```python
# ...
await api.users.get(1)
await bot.api.users.get(1)
await user.api.users.get(1)
```
Рекомендуется использовать IDE с подсказками, так как все методы, ответы и объекты типизированы, а все это полезно только при условии IDE с подсказками

??? danger "Все методы нужно вызывать снейк кейсом:"
      - {--messages.getById--} - **нет**
      - {++messages.get_by_id++} - **да**


#### Респонсы

Как сказано выше все типизировано. В ответе приходят объекты:

```python
# ...
user = await bot.api.users.get(1)
print(user[0].first_name) # Павел
```

## Клавиатуры

Клавиатуры можно генерировать двумя по-своему удобными путями, через специально разработанную схему (`vkbottle.api.keybaord.generator.keyboard_gen`), либо через объективно ориентированный вариант генератора (`vkbottle.api.keyboard.Keyboard`)

### Генератор keyboard_gen

Генератор keyboard_gen является функцией принимающей один обязательный аргумент - схему. Схема является списком со списками со словарями (`List[List[dict]]`)  
Словари на последнем уровне вложенности по сути являеются объектами кнопок в словаре. Они принимают те же параметры что описаны в документации вк, с учетом трех поправок:  

  - вместо `label` **можно** использовать `text`
  - `color` нужно ставить прямо в словаре
  - чтобы указать тип кнопки нужно назначить аргумент `type` в словарь кнопки

#### Пример:

```python
from vkbottle.api.keyboard import keyboard_gen
keyboard = keyboard_gen(
    [
        [{"text": "Кнопка #1", "color": "positive"}, {"text": "Кнопка #2"}], # Это первый ряд кнопок
        [{"type": "location", "text": "Деанон бесплатно"}], # Это второй ряд
    ],
    inline=True,
)
```

### Генератор  Keyboard

Та же самая клавиатура на этом генераторе:

```python
from vkbottle.api.keyboard import Keyboard, Text, Location
keyboard = Keyboard(inline=True)
keyboard.add_row()
keyboard.add_button(Text("Кнопка #1"), color="positive")
keyboard.add_button(Text("Кнопка #2"))
keyboard.add_row()
keyboard.add_button(Location("Деанон бесплатно"))
# keyboard.generate()
```

В обоих генераторах доступны для назначения аргументы:
 
  - **one_time** - если True, клавиатура исчезнет после первого использования  
  - **inline** - если True, клавиатура будет прикреплена к сообщению

Генерацию клавиатуры можно ускорить благодаря установке модулей для работы с json: `ujson`, `hyperjson`, `orjson`

## Uploader (раздел не закончен)

На данный момент доступно только загрузчики для фотографий и документов, но написать нужный не составит никакого труда при минимальных знаниях  

Для начала работы с любым аплоадером, нужно его импортировать. На примере аплоадера для картинок:

```python
from vkbottle.api.uploader.photo import PhotoUploader
```

Далее нужно связать его с ботом или юзером с помощью инициализации, так же любой аплоадер принимает аргумент `generate_attachment_strings`, при значении True после загрузки будет возвращаться уже готовая строка для отправления в `attachment`:

```python
from vkbottle.api.uploader.photo import PhotoUploader
from vkbottle.bot import Bot

bot = Bot(...)
photo_uploader  = PhotoUploader(bot, generate_attachment_strings=True)
```

Теперь чтобы получить строку для отправки: `await photo_uploader.upload_message_photo("img.png")`

## Дополнительно

Если метод из по какой то причине еще не был добавлен в vkbottle его можно вызвать с помощью `api.request`:

```python
from vkbottle.bot import Bot, Message

bot = Bot("token")

# Отрывок хендлера:
async def handler(ans: Message):
    a = await bot.api.request("some.newMethod", {"strange": 1}) 
    # В таком случае методы нужно писать в камель кейсе как сказано в документации и респонс возвращается словарем а не объектом
```

## Авторизация с логином и паролем

Если вы хотите авторизоваться с помощью логина и пароля, для этого тоже есть решение:

```python
from vkbottle.user import User
user = User(login="+71234567890", password="123456")
```