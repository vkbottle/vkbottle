# State-Dispenser

StateDispenser'ы нужны чтобы организоввывать веточную систему организации пользователя. Сложное меню - стейты, квиз - стейты, какая-то игра - стейты.

StateDispenser должен имплементировать следующие методы:

## get

Возвращает `StatePeer` (если запись на запрошенный peer_id существует) или `None` (если нет). На вход получает `peer_id`

## set

Делает запись. На вход получает `peer_id` и `state`.

## delete

Удаляет запись. На вход получает `peer_id`

## Работа со стейтами

Получить стейт можно из объекта любого ивента `event.state_peer.state`

Чтобы задать стейт пользователю достаточно воспользоваться вышеупомянутым методом `set`

Ловить пользователей со стейтами в хендлерами можно с помощью `StateRule`. Пример:

```python
from vkbottle_types import BaseStateGroup
from vkbottle.bot import Message, Bot

bot = Bot("t")

class SuperStates(BaseStateGroup):
    AWKWARD_STATE = 0
    CONFIDENT_STATE = 1
    TERRIFYING_STATE = 2

@bot.on.message(state=SuperStates.AWKWARD_STATE)  # StateRule(SuperStates.AWKWARD_STATE)
async def awkward_handler(message: Message):
    await message.answer("oi awkward")

@bot.on.message(lev="/die")
async def die_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, SuperStates.AWKWARD_STATE)
    return "ok"

bot.run_forever()
```

`set` может принимать `**payload` который позже доступен как словарь из `event.state_peer.payload`

```python
# ... In handler:
await bot.state_dispenser.set(message.peer_id, SuperStates.TERRIFYING_STATE, something=1)
# ... With state:
print(event.state_peer.payload["something"])  # 1
```
