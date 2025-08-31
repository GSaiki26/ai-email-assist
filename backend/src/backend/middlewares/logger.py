from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import Request, Response
from structlog.contextvars import bind_contextvars, unbind_contextvars
from structlog.stdlib import BoundLogger, get_logger

logger: BoundLogger = get_logger()
Next = Callable[[Request], Awaitable[Response]]


async def set_logger(req: Request, call_next: Next) -> Response:
    bind_contextvars(request_id=uuid4().hex, path=req.url)
    logger.info("Request received.")
    res = await call_next(req)

    unbind_contextvars("request_id")
    return res
