from __future__ import annotations

import typing
from collections import UserDict, deque

KT = typing.TypeVar("KT")
VT = typing.TypeVar("VT")

if typing.TYPE_CHECKING:

    class LimitedDict(UserDict[KT, VT]):
        maxlimit: int
        queue: deque[KT]

        def __init__(self, *, maxlimit: int = 1000) -> None: ...

        def set(self, key: KT, value: VT, /) -> typing.Optional[VT]:
            """Set item in the dictionary.
            Returns a value that was deleted when the limit in the dictionary
            was reached, otherwise None.
            """

        def __setitem__(self, key: KT, value: VT, /) -> None: ...

        def __delitem__(self, key: KT) -> None: ...

else:

    class LimitedDict(UserDict, typing.Generic[KT, VT]):
        def __init__(self, *, maxlimit=1000):
            super().__init__()
            self.maxlimit = maxlimit
            self.queue = deque(maxlen=maxlimit)

        def set(self, key, value, /):
            deleted_item = None
            if len(self.queue) >= self.maxlimit:
                deleted_item = self.pop(self.queue.popleft(), None)
            if key not in self.queue:
                self.queue.append(key)
            super().__setitem__(key, value)
            return deleted_item

        def __setitem__(self, key, value, /) -> None:
            self.set(key, value)

        def __delitem__(self, key) -> None:
            if key in self.queue:
                self.queue.remove(key)
            return super().__delitem__(key)


__all__ = ("LimitedDict",)
