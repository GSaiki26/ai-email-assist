import logging
from asyncio import run
from os import environ
from sys import stdin

import structlog
from structlog import configure

from ai_processor.main import main


def setup_logger() -> None:
    log_level = environ.get("LOG_LEVEL", "INFO")
    if not getattr(logging, log_level):
        log_level = "INFO"

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.UnicodeDecoder(),
    ]

    processors.append(
        structlog.dev.ConsoleRenderer() if stdin.isatty() else structlog.processors.JSONRenderer(),
    )

    configure(
        processors,
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level)),
    )


setup_logger()


def _main() -> None:
    run(main())
