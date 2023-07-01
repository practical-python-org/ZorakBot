"""
Arg utils
"""
from __future__ import annotations

import logging
import os
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import OrderedDict

logger = logging.getLogger(__name__)


def add_boolean_arg(parser: ArgumentParser, name: str, desc: str, default: bool = False) -> None:
    """Adds a boolean arg to the arg parser allowing
    --arg and --no-arg for True and False respectively

    Parameters
    ----------
    parser : ArgumentParser
        Arg parser to add the argument to
    name : str
        Name of the argument
    desc : str
        Description of the arg to add
    default : bool, optional
        Default value of the boolean flag, by default False
    """
    dest = name.replace("-", "_")
    group = parser.add_argument_group(f"{name} options:", desc)
    me_group = group.add_mutually_exclusive_group(required=False)
    me_group.add_argument(f"--{name}", dest=dest, action="store_true", help="(default)" if default else "")
    me_group.add_argument(
        f"--no-{name}",
        dest=dest,
        action="store_false",
        help="(default)" if not default else "",
    )
    parser.set_defaults(**{dest: default})


@dataclass
class Args:
    """Data Class for storing CL args"""

    discord_token: str | None = os.getenv("DISCORD_TOKEN", None)
    log_level: int = int(os.getenv("LOGGING_LEVEL", 20))
    server_settings_path: str | None = os.getenv("SERVER_SETTINGS_PATH", None)
    console_log: bool | None = bool(os.getenv("STREAM_LOGS", None))
    drop_db: bool = False


def parse_args() -> Args:
    """Parses CL args into a Args object
    Returns
    -------
    Args
        Args object containing all the
    """
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-ll",
        "--log-level",
        default=logging.INFO,
        type=int,
        dest="log_level",
        help="The log level of logging",
    )
    arg_parser.add_argument(
        "-dt",
        "--discord-token",
        type=str,
        dest="discord_token",
        help="Token for the discord bot connection. " "If not included the TOKEN env variable is used.",
    )
    arg_parser.add_argument(
        "-ssp",
        "--server-settings-path",
        type=str,
        dest="server_settings_path",
        default=os.getenv("SERVER_SETTINGS_PATH", None),
        help="Path to the server settings file. " "If not included the SERVER_SETTINGS_PATH env variable is used.",
    )
    arg_parser.add_argument(
        "-cl", "--console-log", dest="console_log", type=bool, default=None, help="Whether to stream logs to the console. "
    )
    arg_parser.add_argument("-dd", "--drop-db", dest="drop_db", type=bool, default=False, help="Whether to drop the database on startup.")
    return Args(**OrderedDict(vars(arg_parser.parse_args())))
