from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Any, Callable, Optional

__all__ = ("to_async",)


class to_async:
    def __init__(self, *, executor: Optional[ThreadPoolExecutor] = None):
        self.executor = executor

    def __call__(self, blocking: Callable[..., Any]) -> Any:
        @wraps(blocking)
        async def wrapper(*args: Any, **kwargs: Any):
            loop: "asyncio.AbstractEventLoop" = asyncio.get_event_loop()
            if self.executor is None:
                self.executor = ThreadPoolExecutor()

            func = partial(blocking, *args, **kwargs)

            return await loop.run_in_executor(self.executor, func)

        return wrapper
