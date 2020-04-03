class VKError(Exception):
    pass


class TokenGeneratorError(VKError):
    pass


class KeyboardError(VKError):
    pass


class BranchError(Exception):
    pass


class HandlerError(VKError):
    pass


class HandlerReturnError(HandlerError):
    pass
