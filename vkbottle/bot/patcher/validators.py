"""Read LICENSE.txt"""


class RegexValidators:
    def __init__(self):
        pass

    async def int(self, text):
        if text.isdigit():
            return int(text)
        return

    async def float(self, text):
        try:
            a = float(text)
            return a
        except ValueError:
            return

