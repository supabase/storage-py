import asyncio
from typing import Any, Callable, Coroutine

from httpx import AsyncClient as AsyncClient  # noqa: F401
from httpx import Client as BaseClient


class AsyncFinalizerFactory:
    def __init__(self, finalizer: Callable[[], Coroutine[Any, Any, None]]):
        def func():
            event_loop = asyncio.get_event_loop_policy().get_event_loop()
            return event_loop.run_until_complete(finalizer())

        self.finalizer = func


class SyncFinalizerFactory:
    def __init__(self, finalizer: Callable[[], None]):
        self.finalizer = finalizer


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()
