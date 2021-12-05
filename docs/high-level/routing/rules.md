# Rules

## Labeler Custom Rules

- `from_chat` - от `PeerRule`
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

### Внимание!
> Все встроенные рулзы работают только с объектом `Message`, для обработки сырых евентов нужно писать свою реализацию.

Посмотреть логику рулзов можно здесь: [тык](https://github.com/vkbottle/vkbottle/blob/master/vkbottle/dispatch/rules/base.py)
