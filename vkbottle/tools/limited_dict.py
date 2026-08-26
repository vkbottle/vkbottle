from __future__ import annotations

from collections import UserDict, deque

import typing_extensions as typing

KT = typing.TypeVar("KT", default=typing.Any)
VT = typing.TypeVar("VT", default=typing.Any)

if typing.TYPE_CHECKING:
    MutableDictFactory = typing.Callable[..., typing.MutableMapping[KT, VT]]

    class LimitedDict(UserDict[KT, VT]):
        maxlimit: int
        queue: deque[KT]
        data: typing.MutableMapping[KT, VT]  # type: ignore

        @typing.override
        def __init__(
            self,
            *,
            maxlimit: int = 1_000,
            dict_factory: MutableDictFactory[KT, VT] = ...,
        ) -> None: ...

        def set(self, key: KT, value: VT, /) -> VT | None:
            """Set item in the dictionary.
            Returns the oldest value that was deleted when the limit in the dictionary
            was reached, otherwise None.
            """

        def delete_oldest_pair(self) -> tuple[KT, VT] | None:
            """Delete and return the oldest key-value pair, if any."""

        def get_oldest_pair(self) -> tuple[KT, VT] | None:
            """Return the oldest key-value pair, if any."""

        @typing.override
        def __setitem__(self, key: KT, item: VT) -> None: ...

        @typing.override
        def __delitem__(self, key: KT) -> None: ...

else:

    class LimitedDict(UserDict, typing.Generic[KT, VT]):
        def __init__(self, *, maxlimit=1000, dict_factory=dict):
            super().__init__()

            self.data = dict_factory()
            self.maxlimit = maxlimit
            self.queue = deque(maxlen=maxlimit)

        def set(self, key, value, /):
            deleted_item = None

            if key not in self.data:
                if len(self.queue) >= self.maxlimit:
                    deleted_item = self.delete_oldest_pair()[1]

                self.queue.append(key)

            self.data[key] = value
            return deleted_item

        def get_oldest_pair(self):
            if not self.data or not self.queue:
                return None

            key = self.queue[0]
            return key, self.data[key]

        def delete_oldest_pair(self):
            if not self.queue:
                return None

            key = self.queue.popleft()
            return key, self.data.pop(key)

        def __setitem__(self, key, value, /) -> None:
            self.set(key, value)

        def __delitem__(self, key) -> None:
            if key in self.queue:
                self.queue.remove(key)

            self.data.__delitem__(key)


__all__ = ("LimitedDict",)
