from asyncio import Semaphore, get_event_loop, sleep
from typing import Any

from aiohttp import (
    ClientConnectionError,
    ClientResponse,
    ClientResponseError,
    ClientSession,
    ClientTimeout,
)
from structlog.contextvars import bind_contextvars, unbind_contextvars
from structlog.stdlib import BoundLogger, get_logger

from ai_processor.settings import HTTPSettings

logger: BoundLogger = get_logger()


class HTTPClient:
    def __init__(self, settings: HTTPSettings, **kwargs: Any) -> None:  # noqa: ANN401
        self._session = ClientSession(timeout=ClientTimeout(settings.timeout_secs), **kwargs)
        self._sem = Semaphore(settings.concurrency)
        self._cooldown_secs = settings.cooldown_secs

    def __del__(self) -> None:
        loop = get_event_loop()
        self._deletion_task = loop.create_task(self.close())

    async def close(self) -> None:
        logger.debug("Closing HTTP session...", obj=self)
        await self._session.close()
        logger.debug("HTTP session closed.", obj=self)

    async def send(self, **kwargs: Any) -> ClientResponse:  # noqa: ANN401
        bind_contextvars(method=kwargs.get("method"), url=kwargs.get("url"))
        logger.debug("Sending HTTP request...", **kwargs)

        try:
            response = await self._send(**kwargs)
        except (ClientConnectionError, ClientResponseError, Exception) as err:
            logger.debug("HTTP request failed.", exc_info=err)
            unbind_contextvars("method", "url")
            raise

        logger.debug("HTTP request completed.", status_code=response.status)
        unbind_contextvars("method", "url")
        return response

    async def _send(self, **kwargs: Any) -> ClientResponse:  # noqa: ANN401
        was_locked = self._sem.locked()

        async with self._sem:
            if was_locked:
                logger.debug("Semaphore was locked. Waiting for cooldown...")
                await sleep(self._cooldown_secs)

            return await self._session.request(**kwargs)
