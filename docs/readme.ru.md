## Инструкции по посадке

Установка и другие первоэтапные действия описаны в [README.md](/README.md)

Нужные нам классы:

```python
from vkbottle import Bot, Message, keyboard_generator, VKError
```

## Переменные первой ступени:

`session` - aiohttp ClientSession  
`plugin_folder` - string, bot folder name  
`patcher` -  bot patching class, needed for whitelist support  
`on` - main class for decorators
`api` - VK Api wrapper

## Callback!

Мы можем создать простой обработчик событий фласком

```
# app = Flask()
@app.route('/')
def route():
    bot.process(flask.request.args(), confirmation_token='YourConfirm')
```

Это решение помогает сохранять совместимость с процессом совмещения держания бота и сайта на одном адресе

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
@bot.on.message_chat(text='привет')
async def wrapper(ans: Message):
    await ans('Ну привет (всем)!')
```

### Message - ans

Message - простой типизационный датакласс, так же с ним доступны методы:  

`__call__` - простой вызов для написания сообщения в уже сохраненный диалог  
`reply` - ответ на сообщение с уже сохраненным id сообщения

### События

```python
@bot.on.event(name='on_group_join')
async def wrapper(ans: Message):
    try:
        await ans('Удачно ты зашел!')
    except VkError:
        # Нет возможности написать сообщение
        pass
```

### Класс декоратора сообщения

Вы можете использовать startswith и regex:

Startswith:

```python
@bot.on.message.startswith(text='привет')
async def wrapper(ans: Message):
    await ans('твое сообщение началось с <<привет>>')
```

Regex:

```python
@bot.on.message_chat.startswith('.*?')
async def wrapper(ans: Message):
    await ans('этот декоратор сработает при каждом сообщении из чата (зач?)')
```

### Кнопки

Чтобы make кнопки в вашем сообщении just примените генератор или будьте уродами и не используйте его:

1) Составим паттерн:
   Наш список должен состоять из рядов с кнопками:  
   
   ```python
   pattern = [[{'text': 'моя кнопка'}]]
   ```
   
   Вместе с `text` можно передавать все параметры доступные для кнопок из официальной документации

2) Создадим клавиатуру

```python
my_keyboard = keyboard_generator(pattern, one_time=False)
```

3) Отправим ее

```python
@bot.on.message(text='клавиатуру пожалуйста')
async def wrapper(ans: Message):
    await ans('держите', keyboard=keyboard)
```

### Другие декораторы

**@bot.on.chat_mention()**  
Срабатывает при чистом упоминании бота в чате

**@bot.on.chat_invite()**  
Срабатывает при добавлении бота в чат

Кстати, реакции на сообщения работают при упоминании бота в чате через @ 

### :heartpulse: Args in messages handlers

```python
@bot.on.message('меня зовут <name>')
async def wrapper(ans: Message, name):
    await ans(f'Ну привет, {name}!')
```

It works such this in other decorators too (except of regex decorator, of course)
