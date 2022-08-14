from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

LOG_FILE = Path("info_logs.log")
ERR_FILE = Path("err_logs.log")
LOGGER_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def setup_logger(
    level: int = logging.INFO,
    stream_logs: bool = False,
    log_file: Path = LOG_FILE,
    err_file: Path = ERR_FILE,
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

    handler = logging.FileHandler(log_file, mode="w")
    handler.setFormatter(log_formatter)
    handler.setLevel(level)
    handlers.append(handler)

    err_handler = logging.FileHandler(err_file, mode="w")
    err_handler.setFormatter(log_formatter)
    err_handler.setLevel(logging.ERROR)
    handlers.append(err_handler)

    logging.basicConfig(level=level, handlers=handlers)
