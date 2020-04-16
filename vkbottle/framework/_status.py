from ..utils import logger


class LoggerLevel:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        level_no = logger.level(self.level).no
        return record["level"].no >= level_no


class BotStatus:
    polling_started: bool = False
    dispatched: bool = False
    handler_return_context: dict = {}
    middleware_expressions: bool = True

    @property
    def as_dict(self) -> dict:
        return {"polling_started": self.polling_started, "dispatched": self.dispatched}

    def change_handler_return_context(
        self,
        attachment: str = None,
        keyboard: dict = None,
        template: dict = None,
        **params
    ):
        local = locals()
        local.pop("self")
        self.handler_return_context = {k: v for k, v in local.items() if v is not None}
        return self.handler_return_context

    def __repr__(self):
        return str(self.as_dict)
