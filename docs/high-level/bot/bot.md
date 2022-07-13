# Bot

Инстанс бота это аддон состоящий из стандартного апи и составляющих фреймворка, так же он умеет запускать лонгпол

Атрибуты:

`bot.api` - [API документация](../../low-level/api/api.md)<br/>
`bot.router` - [Router документация](../../high-level/routing/index.md)<br/>
`bot.labeler`/`bot.on` - [Labeler документация](labeler.md)<br/>
`bot.polling` - [Polling документация](../../low-level/polling/polling.md)<br/>
`bot.callback` - [Callback документация](../../low-level/callback/callback.md)<br/>
`bot.error_handler` - [Error handler документация](../../low-level/exception_handling/error-handler.md)<br/>
`bot.loop_wrapper` - [Loop Wrapper документация](../../tools/loop-wrapper.md)<br/>
`bot.loop` - возвращает _event loop_ который был установлен или получает запущенный

Функции:

## Long Poll API

### bot.run_polling()

Асинхронный запуск longpoll

### bot.run_forever()

Синхронный запуск longpoll. Добавляет `run_polling` в таски `bot.loop_wrapper` и запускает луп в `run_forever`

## Callback API

### bot.setup_webhook()

Устанавливает сервер для `CallbackAPI` в сообщество

### bot.process_event(event)

Передает полученное событие в роутер, для его обработки
