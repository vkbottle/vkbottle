from .template import AbstractTemplate
import typing


class Answer(AbstractTemplate):
    def ready(
        self,
        text: typing.Union[str, typing.List[str]],
        answer: str,
        lower: bool = True,
    ) -> "Answer":
        async def wrapper(*_) -> str:
            return answer

        self.bot.on.message_handler.add_handler(wrapper, text=text, lower=lower)
        return self

    def run(self, skip_updates: bool = True, **kwargs):
        self.bot.run_polling(skip_updates=skip_updates, **kwargs)
