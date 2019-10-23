class ErrorHandler(object):
    def __init__(self):
        self._error_processors = dict()

    def __call__(self, *error_numbers):
        def decorator(func):
            for error_number in error_numbers:
                self._error_processors[error_number] = {"call": func}
            return func

        return decorator

    def get_processor(self):
        return self._error_processors
