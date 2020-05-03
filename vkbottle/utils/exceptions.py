import typing


class VKError(Exception):
    def __init__(
        self,
        error_code: int,
        error_description: str,
        method_requested=None,
        params_requested: typing.Optional[dict] = None,
    ):
        self.error_code = error_code
        self.error_description = error_description
        self.method_requested = method_requested
        self.params_requested = params_requested

    def __repr__(self):
        return f"<VKError error_code={self.error_code} error_description={self.error_description}>"


class TokenGeneratorError(Exception):
    pass


class KeyboardError(Exception):
    pass


class BranchError(Exception):
    pass


class HandlerError(Exception):
    pass


class HandlerReturnError(HandlerError):
    pass
