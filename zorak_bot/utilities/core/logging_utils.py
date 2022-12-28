from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

LOGGER_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def setup_logger(
    level: int = logging.INFO,
    stream_logs: bool = False,
    logger_format: str = LOGGER_FORMAT,
) -> None:
    """Sets up the service logger
    Parameters
    ----------
    level : int, optional
        Level to log in the main logger, by default logging.INFO
    stream_logs : bool, optional
        Flag to stream the logs to the console, by default False
    logger_format : str, optional
        Format the logger will log in, by default LOGGER_FORMAT
    """
    log_formatter = logging.Formatter(logger_format)

    handlers: list[logging.Handler] = []
    if stream_logs:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        stream_handler.setLevel(level)
        handlers.append(stream_handler)

    logging.basicConfig(level=level, handlers=handlers)
