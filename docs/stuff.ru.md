# Документация по использованию основных воркеров

## Middleware

Middleware (мидлвари далее) используются как первичная обработка, с помощью них можно, например:

* Не обрабатывать сообщения от ботов
* Регистрировать пользователя и возвращать в хендлер как обязательный аргумент
* Записывать статистику

Все примеры будут разобраны ниже

### Не обрабатывать сообщения от ботов

Создадим простой мидлварь, который будет возвращать `False` если источник сообщения - бот, а не пользователь:

```python
from vkbottle.bot import Bot, Message
from vkbottle.ext import Middleware

bot = Bot("token")

@bot.middleware.middleware_handler()
class NoBotMiddleware(Middleware):
    async def middleware(self, message: Message):
        if not message.from_user:
            return False

@bot.on.message_handler(text="тест")
async def wrapper(ans: Message):
    await ans("Работаю только для юзеров")

bot.run_polling()
```

Если сообщение будет отправлено не юзером то бот не будет его обрабатывать

### Регистрировать пользователя и возвращать в хендлер как обязательный аргумент

```python
from vkbottle.bot import Bot, Message
from vkbottle.ext import Middleware
import typing

bot = Bot("token")
database: typing.Dict[int, str] = {}  # Наш прототип базы данных

@bot.middleware.middleware_handler()
class RegistrationMiddleware(Middleware):
    async def middleware(self, message: Message):
        if message.from_id not in database:
            database[message.from_id] = message.text
        return database[message.from_id]

@bot.on.message_handler(text="привет", lower=True)
async def wrapper(ans: Message, first_message: str):
    await ans(f"Я все помню, твое первое сообщение: <<{first_message}>>")

bot.run_polling()
```

### Записывать статистику

```python
from vkbottle.bot import Bot, Message
from vkbottle.ext import Middleware
import typing

bot = Bot("token")
poor_statistics: typing.List[int] = []

@bot.middleware.middleware_handler()
class StatisticsMiddleware(Middleware):
    async def middleware(self, message: Message):
        user = (await bot.api.users.get(user_ids=message.from_id))[0]
        poor_statistics.append(user.sex)

@bot.on.message_handler(text="стат")
async def wrapper(ans: Message):
    stat = (sum(poor_statistics) / len(poor_statistics)) - 1
    await ans(f"{round(stat * 100, 2)} пользователей бота - девочки")

bot.run_polling()
```

### Грызем провода

Если вам по какой-то причине нужно возвращать boolean тип из хендлеров вы можете отключить это:

```python
bot.status.middleware_expressions = False
```

## Error Handler для ошибок из вк

```python
@bot.error_handler(1, 2, 3)
async def error_handler(e):
    print("Ошибки пойманы!", e)
```

P.S. Скоро будет нормальный error handler. stay tuned
