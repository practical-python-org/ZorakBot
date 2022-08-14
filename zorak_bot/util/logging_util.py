from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

LOGGER_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def setup_logger(
    log_file: Path | None,
    err_file: Path | None,
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
    log_file : Path, optional
        Default logger file path, by default LOG_FILE
    err_file : Path, optional
        Error logger file path, by default ERR_FILE
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
    
    if log_file is not None:
        handler = logging.FileHandler(log_file, mode="w")
        handler.setFormatter(log_formatter)
        handler.setLevel(level)
        handlers.append(handler)

    if err_file is not None:
        err_handler = logging.FileHandler(err_file, mode="w")
        err_handler.setFormatter(log_formatter)
        err_handler.setLevel(logging.ERROR)
        handlers.append(err_handler)

    logging.basicConfig(level=level, handlers=handlers)
