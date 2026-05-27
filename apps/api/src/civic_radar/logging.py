"""Structured logging configuration via structlog."""

from __future__ import annotations

import logging
import sys
from typing import Literal

import structlog
from structlog.types import EventDict, Processor


def _drop_color_message(_: object, __: str, event_dict: EventDict) -> EventDict:
    event_dict.pop("color_message", None)
    return event_dict


def configure_logging(
    level: str = "INFO",
    format_: Literal["console", "json"] = "console",
) -> None:
    """Configure structlog + stdlib logging for the application."""

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        _drop_color_message,
    ]

    if format_ == "json":
        renderer: Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=sys.stderr.isatty())

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=level.upper(),
        format="%(message)s",
        stream=sys.stderr,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)  # type: ignore[no-any-return]
