# Bot

Инстанс бота состоит из стандартного апи, лонгпола и других частей фреймворка.

Атрибуты:

`bot.api` - [API документация](../low-level/api.md)<br/>
`bot.router` - [Router документация](../high-level/handling/router.md)<br/>
`bot.labeler`/`bot.on` - [Labeler документация](bot/labeler.md)<br/>
`bot.polling` - [Polling документация](../low-level/polling.md)<br/>
`bot.callback` - [Callback документация](../low-level/callback.md)<br/>
`bot.error_handler` - [Error handler документация](../low-level/exception_handling/error-handler.md)<br/>
`bot.loop_wrapper` - [Loop Wrapper документация](../tools/loop-wrapper.md)<br/>

Функции:

## Long Poll API

### `bot.run_polling()`

Асинхронный запуск longpoll

### `bot.run_forever()`

Синхронный запуск longpoll. Добавляет `run_polling` в таски `bot.loop_wrapper` и вызывает `bot.loop_wrapper.run()`

## Callback API

### `bot.setup_webhook()`

Устанавливает сервер для `CallbackAPI` в сообщество

### `bot.process_event(event)`

Передает полученное событие в роутер, для его обработки
