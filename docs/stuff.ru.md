# Документация по использованию основных воркеров

## Middleware

Middleware (мидлвари далее) используются как первичная обработка, с помощью них можно, например:

* Не обрабатывать сообщения от ботов
* Регистрировать пользователя и возвращать в хендлер как обязательный аргумент
* Записывать статистику

Все примеры будут разобраны ниже

**ВНИМАНИЕ!** С версии `2.7.5` Middleware должен имплементить методы `pre` и `post`, а не `middleware`, как было раньше. Если вы пользуетесь версией ниже `2.7.5` замените `pre` на `middleware`, а от post придется воздержаться

### Не обрабатывать сообщения от ботов

Создадим простой мидлварь, который будет возвращать `False` если источник сообщения - бот, а не пользователь:

```python
from vkbottle.bot import Bot, Message
from vkbottle.ext import Middleware

bot = Bot("token")

@bot.middleware.middleware_handler()
class NoBotMiddleware(Middleware):
    async def pre(self, message: Message, *args):
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
    async def pre(self, message: Message):
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
    async def pre(self, message: Message):
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

### Error Handler

Для того чтобы хендлить ошибки вк без выбрасывания исключения можно воспользоваться `error_handler`. Он отлично подойдет для, например, решения капчи или delay для методов которые привысили лимит (частая проблема для пользователей User Longpoll)

Для того чтобы добавить простейший хендлер ошибки можно воспользоваться декоратором:

```python
from vkbottle.user import User, Message
from vkbottle.exceptions import VKError
from asyncio import sleep

user = User("token")

@user.error_handler.error_handler(6)
async def rps_handler(e: VKError):
    await sleep(1)
    await e.method_requested(**e.params_requested)
```

Для того чтобы добавить решение капчи существует специальный хендлер `captcha_handler`, он должен возвращать код от решенной капчи:

```python
@user.error_handler.captcha_handler
async def solve_captcha(e: VKError):
    key = "Здесь вы решаете капчу и возвращаете код"
    return key
```

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
