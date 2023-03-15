# MessageEvent

Обработка `callback` кнопок выходит на новый уровень:

```python
from vkbottle import GroupEventType
from vkbottle.bot import MessageEvent

@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def handle_message_event(event: MessageEvent):
    await event.show_snackbar("Сейчас я исчезну")
```

* Никакого `object`. Всё находится уже в `event`, вместе с `group_id`
* Поддержка всех генераторов `event-data` при помощи соответствующими функциями
* Поддержка рулзов, связанных с `payload`
* Так же есть `message_edit` и `message_send`

## Старый способ

```python
from vkbottle import GroupEventType, GroupTypes, ShowSnackbarEvent

@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_message_event(event: GroupTypes.MessageEvent):
    await event.ctx_api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=ShowSnackbarEvent(text="Сейчас я исчезну").json(),
    )
```

[Полноценный пример](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/callback_buttons.py)
