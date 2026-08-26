# Все встроенные правила

---

## PeerRule

`PeerRule(from_chat: bool = True)`

Нужно для ограничения источника сообщения, `PeerRule(from_chat=False)` например, будет указывать на то, что сообщение должно быть из личного диалога с ботом.

---

## MentionRule

`MentionRule(mention_only: bool = False)`

Используется для проверки на то, что бот был упомянут в сообщении. Параметр `mention_only` используется чтобы указать, что кроме упоминания в сообщении быть ничего не должно, в ином случае из сообщения удаляется упоминание чтобы другие правила могли обработать уже сам текст.

---

## CommandRule

```python
CommandRule(command_text, prefixes, args_count=0, sep=" ")
```

Используется для того чтобы реагировать на команды

Команда выглядит так:

```
{prefix}{command_text}{sep.join(args)}
```

В `command_text` можно передать несколько вариантов названия команды.

В `prefixes` можно передать несколько возможных префиксов (например: '/', '!').

В `args_count` передается количество обязательных аргументов с `sep` в качестве разделителя

---

## VBMLRule

```python
VBMLRule(pattern, patcher=None, flags=None)
```

Используется в качестве парсера текстов сообщений. Разметка vbml исторически была сделана специально для фреймворка, чтобы легко писать паттерны с валидируемыми аргументами.

Пример:

```python
rule = VBMLRule("/cmd <eggs:int>")
rst = await rule.check(Message(text="/cmd 11", ...))
assert rst == {"eggs": 11}
```

Больше документации [CLICK 🤩](https://github.com/tesseradecade/vbml/blob/master/docs/index.md)

---

## RegexRule

`RegexRule(regexp)`

Используется для проверки на соответствие текста сообщения регулярному выражению.

---

## StickerRule

`StickerRule(sticker_ids = None)`

Используется для того чтобы отлавливать отправку стикеров в сообщении. Если sticker_ids = None, то проходить будет любое сообщение содержащее стикер.

---

## FromPeerRule

`FromPeerRule(peer_ids)`

Используется для отлова сообщений отправленных пользователем/группой с одним из указанных ID.

---

## AttachementTypeRule

`AttachementTypeRule(attachment_types)`

Используется для отлова сообщений с указанным типом вложений (например: `photo`)


---

## ForwardMessagesRule

Используется для того, чтобы проверить, что сообщение содержит в себе вложенные сообщения.

---

## ReplyMessageRule

`ReplyMessageRule(reply_message: bool = True)`

--

## GeoRule

Используется для того чтобы отлавливать сообщения с геометкой.

## LevenshteinRule

!!! info "Deprecation"
    На данный момент обсуждается удаление этого правила из новых версий из-за его неоптимальности. Вместо этого рекомендуется использовать `FuzzyTextRule`

`LevenshteinRule(levenshtein_texts, max_distance: int = 1)`

Используется для fuzzy string matching'а.

Может принимать max_distance - максимальное отклонение от заданного текста.

## FuzzyTextRule

`FuzzyTextRule(texts, min_ratio: float = 0.7)`

Используется для fuzzy string matching'а.

Настраивается через min_ratio - минимальная _похожесть_ сообщения с переданным текстом (от 0 до 1).

## MessageLengthRule

`MessageLengthRule(min_length: int)`

Используется для ограничения минимальной длины текстового сообщения.

## ChatActionRule

`ChatActionRule(chat_action_types)`

Используется для отлова событий в беседах (например: `chat_invite_user`). [Документация ВК по chat actions](https://dev.vk.ru/reference/objects/message#action)

## PayloadRule

`PayloadRule(payload)`

Проверяет что у сообщения payload равен одному из данных.

## PayloadContainsRule

`PayloadContainsRule(payload_part)`

Проверяет что в payload сообщения содержит данную часть.

## PayloadMapRule

`PayloadMapRule(payload_map)`

Используется для создания ассоциаций необходимых значений и типов в payload сообщений

Например:

Такой payload как:

```json
{"name": "boba", "data": {"action": "do", "number": 12}}
```

Выражается таким payload map:

```python
PayloadMapRule({"name": str, "data": {"action": str, "number": int}})
```

Вместо типа данных так же можно передать валидатор (`ABCValidator`), функцию (она будет вызвана со значением из полезной нагрузки сообщения) или literal-значения, например, если `"name"` в полезной нагрузке должен быть всегда `"boba"`, можно указать нужное значение в маппинге.

Пример:

```python
PayloadMapRule(
    {
        "name": "boba",
        "data": {
            "action": lambda x: x in ("do", "undo"),
            "number": int,
        },
    }
)
```

## FromUserRule

`FromUserRule(from_user: bool = True)`

Используется для проверки что сообщение было отправлено пользователем, а не ботом.

При `from_user = False`, работает в обратную сторону, проверяет что сообщение отправлено ботом.

## FuncRule

`FuncRule(func)`

Принимает функцию, которая будет вызвана с единственным аргументом - событием. Функция должна вернуть bool или dict с обновлением контекста.

## CoroutineRule

`CoroutineRule(coro)`

Ответ проверки правила получается из переданной корутины.

## StateRule

`StateRule(state)`

Нужно для стейт-машины, проверяет что источник ивента находится в переданном состоянии.

Если переданное состояние = None, то правило проверяет чтобы источник не находился ни в каком состоянии.

## StateGroupRule

`StateGroupRule(state_group)`

Проверяет что пользователь находится в нужной коллекции состояний.
