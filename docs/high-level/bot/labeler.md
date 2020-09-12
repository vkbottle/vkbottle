# Bot-Labeler

Удобная оболочка над роутерами. С помощью лейблера создаются хендлеры. Может быть использовано в качестве портабельного диспатчера.

Имеет метод load который должен загружать хендлеры и мидлвари в текущий лейблер из данного. Может быть использовано для разбивания кода на много частей:

__bot.py__
```python
from vkbottle import Bot
from routes import labelers

bot = Bot("token")

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.run_forever()
```

__routes/\_\_init\_\_.py__
```python
from . import greetings, goodbyes

labelers = [greetings.bl, goodbyes.bl]
```

__routes/greetings.py__
```python
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

@bl.message(text=["привет", "хай", "здравствуй"])
async def greeting(message: Message):
    await message.answer("Привет, друг")
```

__routes/goodbyes.py__
```python
from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()

@bl.message(text=["пока", "до свидания"])
async def greeting(message: Message):
    await message.answer("До новых встреч")
```