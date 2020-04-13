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

Хороший пример с генератором: [examples/tests/user/shuffle_tokens.py]()

**throw_errors** определяет стандартное поведение API. После,  он может быть переопределен только при вызове собственно метода

**tokens** - может быть как списком токенов,  так и одним токеном. В ботах рекомендуется использовать до 2 токенов (максимальная нагрузка - 40 запросов в секунду), тогда как при работе с юзерами может понадобится больше 6 из-за невероятно низкого лимита (3 запроса в секунду)

### Bot API, User API
Для вызова API методов с инициированным ботом потребуется использовать атрибут класса `Bot.api`:

```python
from vkbottle.bot import Bot
from vkbottle.user import User
from vkbottle.api.api.builtin import LimitedTokenGenerator

bot_token = "token-1"
user_tokens = ["user-token-1", "user-token-2", "user-token-3"]
user_generator = LimitedTokenGenerator(user_tokens, limit=3)

bot = Bot(tokens=token, throw_errors=False)
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

**ВСЕ МЕТОДЫ ПЕРЕВЕДЕНЫ В СНЕЙК КЕЙС** (getById => get_by_id)


#### Респонсы

Как сказано выше все типизировано. В ответе приходят объекты:

```python
# ...
user = await bot.api.users.get(1)
print(user[0].first_name) # Павел
```
