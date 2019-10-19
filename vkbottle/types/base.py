import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        allow_mutation = False
        use_enum_values = True

    def __str__(self):
        return str(self.dict(skip_defaults=True))

    def __repr__(self):
        args = ", ".join(
            [f"{key}={value}" for key, value in self.dict(skip_defaults=True).items()]
        )
        return "{}({})".format(self.__class__.__name__, args)
