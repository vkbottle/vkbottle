class VKError(Exception):
    pass


class FetchMethodError(Exception):
    pass


class MailingAPIError(Exception):
    pass


class BranchError(Exception):
    pass


class HandlerError(Exception):
    pass


class HandlerReturnError(HandlerError):
    pass


class VBMLError(Exception):
    pass
