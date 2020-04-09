from .filter import AbstractFilter


class OrFilter(AbstractFilter):
    async def check(self, event) -> bool:
        for rule in self.rules:
            if await rule.check(event):
                return True


class AndFilter(AbstractFilter):
    async def check(self, event) -> bool:
        for rule in self.rules:
            if not await rule.check(event):
                return False
        return True


class AnyFilter(AbstractFilter):
    async def check(self, event) -> bool:
        return any([await rule.check(event) for rule in self.rules])


class AllFilter(AbstractFilter):
    async def check(self, event) -> bool:
        return all([await rule.check(event) for rule in self.rules])
