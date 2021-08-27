from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Optional, Type

AsyncFunc = Callable[..., Awaitable[Any]]


class ABCErrorHandler(ABC):
    error_handlers: Dict[Type[BaseException], AsyncFunc]
    undefined_error_handler: Optional[AsyncFunc]

    @abstractmethod
    def register_error_handler(
        self, *error_types: Type[BaseException]
    ) -> Callable[[AsyncFunc], AsyncFunc]:
        pass

    @abstractmethod
    def register_undefined_error_handler(self, handler: AsyncFunc) -> AsyncFunc:
        pass

    @abstractmethod
    async def handle(self, error: BaseException) -> Any:
        pass

    @abstractmethod
    def catch(self, func: AsyncFunc) -> AsyncFunc:
        pass
