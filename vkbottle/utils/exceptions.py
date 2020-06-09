import typing


class VKError(Exception):
    def __init__(
        self,
        error_code: int,
        error_description: str,
        method_requested=None,
        params_requested: typing.Optional[dict] = None,
        raw_error: typing.Optional[dict] = None,
    ):
        self.error_code = error_code
        self.error_description = error_description
        self.method_requested = method_requested
        self.params_requested = params_requested
        self.raw_error = raw_error

    def __repr__(self):
        return f"<VKError error_code={self.error_code} error_description={self.error_description}>"


class TokenGeneratorError(Exception):
    pass


class KeyboardError(Exception):
    pass


class TemplateError(Exception):
    pass


class BranchError(Exception):
    pass


class HandlerError(Exception):
    pass


class HandlerReturnError(HandlerError):
    pass


class StorageError(Exception):
    pass
