class BotStatus:
    polling_started: bool = False
    dispatched: bool = False
    handler_return_context: dict = {}

    @property
    def readable(self) -> dict:
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
