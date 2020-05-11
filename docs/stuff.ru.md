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

## Error Handler

### Swear

Вы можете хендлить все исключения, которые выбрасываются хендлером с помощью декоратора `swear`:  

```python
from vkbottle.framework import swear
from vkbottle import VKError

async def exc_kick(e: VKError, message: Message):
    await message("Не могу кикнуть =(")

@bot.on.chat_message(commands=["самобан"])
@swear(VKError, exception_handler=exc_kick)
async def self_ban(ans: Message):
    await bot.api.messages.remove_chat_user(ans.chat_id, ans.from_id)
    return "хаха самобан"
```

### Only error
Способ далее является устаревшим, но он применим для всех хендлеров в целом. С помощью него можно например ловить `Rate limit reached`:

```python
@bot.error_handler(29)
async def error_handler(e):
    # 
    print("О нет Rate limit reached, спасите")
```

P.S. Скоро будет нормальный error handler для этого типа

## TaskManager

Если вам нужно начать работу с vkbottle "с нуля" вам может понадобится `TaskManager`

```python
from vkbottle import TaskManager
from vkbottle.api import API

api = API("token")

# Создайте вашу асинхронную функцию для запуска в таск менеджере
# для начала работы с апи
async def main():
    await api.status.set("Я люблю котиков")

task_manager = TaskManager()
# Добавьте нужные таски
task_manager.add_task(main())
task_manager.run()
```

Если таск один, как в прошлом примере, оптимальнее будет воспользоваться методом `run_task`