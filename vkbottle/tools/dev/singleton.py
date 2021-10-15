class Singleton:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is not None:
            return cls.__instance__
        return super().__new__(cls, *args, **kwargs)
