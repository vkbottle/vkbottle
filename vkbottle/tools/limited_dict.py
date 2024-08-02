import typing
from collections import UserDict, deque

KT = typing.TypeVar("KT")
VT = typing.TypeVar("VT")


class LimitedDict(UserDict[KT, VT]):
    def __init__(self, *, maxlimit: int = 1000) -> None:
        super().__init__()
        self.maxlimit = maxlimit
        self.queue: deque = deque(maxlen=maxlimit)

    def set(self, key: KT, value: VT, /) -> typing.Optional[VT]:
        """Set item in the dictionary.
        Returns a value that was deleted when the limit in the dictionary
        was reached, otherwise None.
        """

        deleted_item = None
        if len(self.queue) >= self.maxlimit:
            deleted_item = self.pop(self.queue.popleft(), None)
        if key not in self.queue:
            self.queue.append(key)
        super().__setitem__(key, value)
        return deleted_item

    def __setitem__(self, key: KT, value: VT, /) -> None:
        self.set(key, value)

    def __delitem__(self, key: KT) -> None:
        if key in self.queue:
            self.queue.remove(key)
        return super().__delitem__(key)
