# Rules

## Labeler Custom Rules

- `from_chat` - от `PeerRule`
- `mention` - от `MentionRule`
- `command` - от `CommandRule`
- `from_user` - от `FromUserRule`
- `peer_ids` - от `FromPeerRule`
- `sticker` - от `StickerRule`
- `attachment` - от `AttachmentTypeRule`
- `levenshtein` и `lev` - от `LevenshteinRule`
- `length` - от `MessageLengthRule`
- `action` - от `ChatActionRule`
- `payload` - от `PayloadRule`
- `payload_contains` - от `PayloadContainsRule`
- `payload_map` - от `PayloadMapRule`
- `func` - от `FuncRule`
- `coroutine` и `coro` - от `CoroutineRule`
- `state` - от `StateRule`
- `state_group` - от `StateGroupRule`
- `regexp` и `regex` - от `RegexRule`
- `macro` - от `MacroRule`
- `text` - от `VBMLRule`

!!! warning "Внимание"
    Все встроенные рулзы работают только с объектами `Message` и `MessageEvent` из `vkbottle.bot`, для обработки сырых евентов нужно писать свою реализацию.

Посмотреть логику рулзов можно [здесь](https://github.com/vkbottle/vkbottle/blob/master/vkbottle/dispatch/rules/base.py)
