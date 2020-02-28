## Инструкции по посадке

Установка и другие первоэтапные действия описаны в [README.md](/README.md)

Нужные нам классы:

```python
import typing
from vkbottle import Bot, Message, keyboard_gen, VKError
```

## API

Вызывать встроенное API можно двумя способами:

```python
# ...
await bot.api.request("users.get", {"users_id": 1})
await bot.api.users.get(users_id=1)
```

Получить API:

```python
from vkbottle.api import Api
```

В обоих случаях методы вызываются асинхронно, для синхронного вызова потребуется воспользоваться `TaskManager` (читать [фреймворк документацию](/docs/FrameworkAPI.md))

## Callback!

Мы можем создать простой обработчик событий любым веб-фреймворком (настоятельно рекомендуется использовать асинхронные решения).

```
# app = FrameWork()
@app.route('/')
async def route():
    return await bot.emulate(request.args(), confirmation_token='YourConfirm')
```

Это решение помогает сохранять совместимость с процессом совмещения размещения бота и сайта на одном адресе.

**:cowboy_hat_face: При Callback'е поллинг запускать не надо..**

## Декораторы

### Простой ответ на сообщение:

:star: В личные сообщения:

```python
@bot.on.message(text='привет')
async def wrapper(ans: Message):
    await ans('Ну привет!')
```

:star: В чат:

```python
@bot.on.chat_message(text='привет')
async def wrapper(ans: Message):
    await ans('Ну привет (всем)!')
```

### Message - ans

Message - простой класс для работы с сообщениями пришедшими от пользователя, так же с ним доступны методы:  

`__call__` - простой вызов для написания сообщения в уже известный диалог.
`reply` - ответ на сообщение с уже известным id сообщения.

Помимо всего этого, Вы можете обратиться к различным полям `Message`, например: `Message.text` (подробнее в официальной документации VK-API).

### События

```python
@bot.on.event.group_join()
async def wrapper(event: GroupJoin):
    print('+1')
```

### Кнопки

### Новый способ

```python
from vkbottle.keyboard import Keyboard, Text

keyboard = Keyboard(one_time=True)
keyboard.add_row()
keyboard.add_button(Text(label="моя кнопка"), color="primary")
```

```python
@bot.on.message(text='клавиатуру пожалуйста', lower=True)
async def wrapper(ans: Message):
    await ans('Держите.', keyboard=keyboard.generate())
```

### Старый способ

Чтобы make кнопки в вашем сообщении just примените генератор или будьте уродами и не используйте его:

1) Составим паттерн:
   Наш список должен состоять из рядов с кнопками:  
   
   ```python
   pattern = [[{'text': 'моя кнопка'}]]
   ```
   
   Вместе с `text` можно передавать все параметры доступные для кнопок из официальной документации.

2) Создадим клавиатуру

```python
my_keyboard = keyboard_gen(pattern, one_time=False)
```

3) Отправим ее

```python
@bot.on.message(text='клавиатуру пожалуйста', lower=True)
async def wrapper(ans: Message):
    await ans('Держите.', keyboard=my_keyboard)
```

### Другие декораторы

**@bot.on.chat_mention()**
Срабатывает при простом упоминании бота в чате

**@bot.on.chat_invite()**
Срабатывает при добавлении бота в чат

Кстати, реакции на сообщения работают при упоминании бота в чате через @.

### :heartpulse: Аргументы хендлеров

```python
@bot.on.message(text='меня зовут <name>')
async def wrapper(ans: Message, name):
    await ans(f'Ну привет, {name}!')
```

### Валидаторы

Есть отдельная документация по валидаторам на русском языке, [загляните сюда](/docs/validators-docs.md).
Валидаторы используются в основном для поддержания бота в тонусе и минимизации нагрузки. Валидаторы позволяют вам не проверять является ли какая-то часть сообщения числом или ссылкой, все это встроено. Кроме того вы можете писать свои собственные кастомные валидаторы.

### Ветки (англ. - Branches)

Ветки, так называемые short-term ветки событий, с помощью них вы можете построить систему тестов, ввод какого-то значения пользователем или даже ~~игрового бота~~
Документацию по веткам вы сможете найти [перейдя сюда](/docs/branches.ru.md)

### Правила (англ. - Rules)

Правила обработки сообщений по стандарту обрабатываются с помощью правила VBMLRule (`vkbottle.rule.VBMLRule`), но что если в задачу хендлера входит прием например сообщений с каким-то вложением. Для начала давайте разберемся как работают правила:  
```python
from vkbottle.rule import ChatActionRule
# Импортировали стандартное правило на событие в чате

@bot.on.message(ChatActionRule("chat_invite_user", "chat_invite_user_by_link"))
async def wrapper(ans: Message):
    await ans(f'Ура! Новый участник в нашей беседе')
```

Стандартные правила: `AttachmentRule(attachment_type)`, `ChatActionRule(chat_action_type, required)`, `VBMLRule(pattern/str/list[pattern/str])`, `PayloadRule(payload as dict)`, `EventRule(events)`  
Для создания собственных правил могут понадобиться абстрактные классы: AbstractRule, AbstractMessageRule  

```python
from vkbottle.rule import AbstractMessageRule

# Создаем класс для правила
class OnlyMe(AbstractMessageRule):
    async def check(self, message: Message):
        # Функция check вызывается при проверке правила
        if message.from_id == 1: # Если пользователь, написавший сообщение имеет id = 1
            return True # Проверка пройдена

@bot.on.message(OnlyMe(), text="/admincommand")
async def wrapper(ans: Message):
    await ans("Команда доступна только одному человеку :)")
```

**Советы**

Так же можно использовать функцию `__init__`, которую предусматривает абстрактный класс, с помощью нее можно кастомизировать собственные правила  
Класс в `context` имеет два поля: `args` и `kwargs`, изменяя одно - вы добавляете позиционные аргументы которые будут возвращены в хендлер, другое - непозиционные

Полная документация по правилам ожидает вас [по этой ссылке](/docs/RulesExecutor.md)

### Ошибки

| Название ошибки    | Причина возникновения                           | Способ устранения                                                                 |
|:------------------:|:-----------------------------------------------:|:---------------------------------------------------------------------------------:|
| VKError            | Ошибка в запросах API                           | Прочитать документацию VK и устранить ошибку                                      |
| BranchError        | Ошибка в переадресации в бранч                  | Чаще всего - бранч не указан, указать его                                         |
| HandlerError       | Ошибка в инициализации обработчиков             | Сделать функцию асинхронной                                                       |
| HandlerReturnError | (Наследуется от HandlerError)                   | Хендлер вернул что-то помимо разрешенных типов и объектов бранчей - исправить это |
| VBMLError          | Ошибка в создании паттернов VBML                | Прочитать документацию VBML и исправить ошибку                                    |

Если вы уверены, что в возникновении ошибки нет вашей вины - пишите Issue, в ближайшее время поступит :heart: fix

### Дополнительная документация

Дополнительную документацию по этому и другим разделам можно [найти здесь](/docs/FrameworkAPI.md)
