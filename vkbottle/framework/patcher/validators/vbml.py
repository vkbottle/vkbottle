from urllib import parse


class VBMLValidators:
    def __init__(self):
        pass

    async def int(self, value: str):
        if value.isdigit():
            return int(value)
        return

    async def float(self, value: str):
        try:
            return float(value)
        except ValueError:
            return

    async def url(self, value: str):
        scheme = parse.urlparse(value)
        if scheme.netloc != "":
            return value
        return

    async def validator(self, value: str, *args):
        print(
            "Value {} was validated by default validator! Hold on.\nReceived args: {}".format(
                value, args
            )
        )
        return value
