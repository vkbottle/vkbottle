# Генераторы `event-data`

Документация ко всем объектам `event_data`: [здесь](https://dev.vk.com/api/bots/development/keyboard#Типы%20действий)

## Их реализации в vkbottle

- `ShowSnackbarEvent`
- `OpenLinkEvent`
- `OpenAppEvent`

### Пример использования внутри `raw_event` хендлера

```python
from vkbottle import ShowSnackbarEvent

await api.messages.send_message_event_answer(
    event_id=event.object.event_id,
    user_id=event.object.user_id,
    peer_id=event.object.peer_id,
    event_data=ShowSnackbarEvent(text="Сейчас я исчезну").json(),
)
```

[Этот пример целиком](https://github.com/vkbottle/vkbottle/tree/master/examples/high-level/callback_buttons.py)
