# Rules

## Bot-Labeler Custom Rules

`from_chat` - от `PeerRule`  
`command` - от `CommandRule`  
`from_user` - от `FromUserRule`  
`peer_ids` - от `FromPeerRule`  
`sticker` - от `StickerRule`  
`attachment` - от `AttachmentTypeRule`  
`levenstein` и `lev` - от `LevensteinRule`  
`length` - от `MessageLengthRule`  
`action` - от `ChatActionRule`  
`payload` - от `PayloadRule`  
`payload_contains` - от `PayloadContainsRule`  
`payload_map` - от `PayloadMapRule`  
`func` - от `FuncRule`  

Посмотреть логику рулзов можно здесь: [тык](https://github.com/timoniq/vkbottle/blob/v3.0/vkbottle/dispatch/rules/bot.py)
