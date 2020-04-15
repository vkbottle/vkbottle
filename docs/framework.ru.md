
В каждом отдельном примере этой документации сниппеты кода полностью рабочие

# Боты  
  
Работа с ботами организуется с помощью класса `vkbottle.bot.Bot`. В самом классе предусмотрена встоенная обработка событий, роутинг в хендлеры, обработка ошибок  
  
## Создание бота  
  
Импортируйте нужные компоненты из `vkbottle.bot`, а именно `Bot` и датакласс `Message`:  
  
``` python  
from vkbottle.bot import Bot, Message  
  
bot = Bot("token", debug="DEBUG") # Рассматриваем эту часть
bot.run_polling(skip_updates=True) # О запуске будет написано ниже
```
  
Для кастомизации доступны аргументы:    
  
| Параметр | Описание |  
|--|--|  
| tokens | список токенов / токен |  
| group_id | group_id будет и так получен сам, но если токен не имеет такого права можно его указать самостоятельно |  
| debug | bool / str, уровень логов, по умолчанию `INFO` |
| throw_errors | Стандартный режим для API, указывает на выбрасывание разрешение выброса исключений |
| log_to_path | bool / str, указывает путь к папке для логов |
| patcher | VBML Patcher ([документация здесь](https://github.com/timoniq/vbml)) |
| mobile | bool, True если пользуетесь мобильными компиляторами |
| secret | str, секретный код для callback проверяемый при каждом событии |
| extension | AbstractExtension, нужно для получения random_id, API в датаклассах |

###  Атрибуты бота

| Атрибут | Описание |
|--|--|
| `Bot.group_id` | int, ID группы, полученное или указанное при инициализации |
| `Bot.loop` | asyncio.AbstractEventLoop |
| `Bot.api` | `vkbottle.api.Api`, для работы с API вконтакте |
| `Bot.branch` | Для создания и контроля состояний пользователей ([документация здесь](https://github.com/timoniq/vkbottle/blob/master/docs/branches.ru.md)) |
| `Bot.middleware` | Для создания мидлварей, документация далее |
| `Bot.on` | `vkbottle.framework.handler.Handler` Для добавления хендлеров, документация далее |
| `Bot.error_handler` | Для создания хендлеров ошибок, документация скоро |
| `Bot.status` | - |

## Создание хендлеров

Для создания хендлеров воспользуйтесь атрибутом бота `on`  
Типы хендлеров: `message`, `chat_message` и основной `message_handler`

Хендлеры для `message` и `chat_message` просто добавляют добавляют дополнительные правила: `vkbottle.framework.rule.PrivateMessage` или `vkbottle.framework.rule.ChatMessage`

Для добавления хендлеров в обработчик можно использовать два интерфейса: декораторы и функциональный

Хендлеры принимают любое кол-во правил (`vkbottle.framework.rule`) и **column rules**:

| col rule | Описание |
|--|--|
| text | vbml pattern схема |
| sticker | id стикера |
| commands | прибавл |
| lev / levenstein | расстояние левенштейна (1) |


### Хендлеры через декораторы

Для добавления хендлеров через декораторы используется следующий интерфейс:

``` python  
from vkbottle.bot import Bot, Message  

bot = Bot("token", debug="DEBUG")

@bot.on.message_handler(text="я не <denied> а <accepted>", lower=True)
async def wrapper(ans: Message, denied: str, accepted: str):
	await ans.reply(f"Ты не {denied}, а {accepted}")

bot.run_polling()
```

В любой хендлер всегда возвращается объект события, то есть `Message` в данном случае. Так же вернулись аргументы, возвращаемые из правил, а именно `denied` и `accepted` из `VBMLRule`, представленное в `col rule` `text`

Кроме ***rules** и ****col_rules** существуют еще доп аргументы *(которые возможно будут перенесены или удалены в следующем релизе)*  
А именно:  
**command: bool** - для добавления префиксов к **text** из `Handler.(message_handler).prefix`
**lower: bool** - для того чтобы игнорировать кейс в **text** (`re.IGNORECASE`)

### Добавление хендлера через функцию

``` python  
from vkbottle.bot import Bot, Message  

bot = Bot("token", debug="DEBUG")

async def wrapper(ans: Message, denied: str, accepted: str):
	await ans.reply(f"Ты не {denied}, а {accepted}")

bot.on.message_handler.add_handler(wrapper, text="я не <denied> а <accepted>", lower=True)
bot.run_polling()
```

Кроме выше описанных аргументов, `Handler.(message_handler).add_handler` принимает `func`

### Хендлеры других ивентов

Кроме ивента сообщения в longpoll насчитывается еще 40 событий, все они обрабатываются похожим образом:

``` python  
from vkbottle.bot import Bot, Message  
from vkbottle.types import GroupJoin # Ваше IDE даст вам подсказку по

bot = Bot("token", debug="DEBUG", throw_errors=False)

@bot.on.event.group_join()  
async def wrapper(event: GroupJoin):  
	# Даже если пользователь не разрешил присылать ему сообщения,
	# исключения не будет потому что throw_errors=False
	await bot.api.messages.send(
		peer_id=event.user_id, 
		message="Спасибо за пополнение наших рядов!",
		random_id=bot.extension.random_id()
	)

bot.run_polling()
```

### Хендлеры специальных событий

Примеры всех хендлеров вы можете [найти здесь](https://github.com/timoniq/vkbottle/blob/master/examples/bot_decorators.py)

# Юзеры

Документация скоро будет