"""
The in-house server bot of Practical Python!
- https://discord.gg/vgZmgNwuHw
- https://github.com/practical-python-org/ZorakBot
- Practicalpython-staff@pm.me
"""
import logging
import os

import discord
from discord.ext import commands

from zorak.utilities.core.args_utils import parse_args
from zorak.utilities.core.logging_utils import setup_logger
from zorak.utilities.core.mongo import initialise_bot_db
from zorak.utilities.core.server_settings import Settings

logger = logging.getLogger(__name__)

COGS_ROOT_PATH = os.path.join(os.path.dirname(__file__), "cogs")
logger.debug(f"COG_PATH: {COGS_ROOT_PATH}")

server_settings_path = None


def load_cogs(bot):
    """
    Loads the directories under the /cogs/ folder,
    then digs through those directories and loads the cogs.
    """
    logger.info("Loading Cogs...")
    for directory in os.listdir(COGS_ROOT_PATH):
        if directory.startswith("_"):
            logger.debug(f"Skipping {directory} as it is a hidden directory.")
            continue
        if directory.startswith("debug") and not logger.level == logging.DEBUG:
            logger.debug(f"Skipping {directory} as it is not the debug cog.")
            continue

        cog_subdir_path = os.path.join(COGS_ROOT_PATH, directory)
        for file in os.listdir(cog_subdir_path):
            if file.endswith(".py") and not file.startswith("_"):
                # try:
                cog_path = os.path.join(cog_subdir_path, file)
                logger.info(f"Loading Cog: {cog_path}")
                # try:
                bot.load_extension(f"zorak.cogs.{directory}.{file[:-3]}")
                # except Exception as e:
                #     logger.warning("Failed to load: {%s}.{%s}, {%s}", directory, file, e)
                #     logger.debug(f"Loaded Cog: {cog_path}")
                # except Exception as e:
                #     logger.warning("Failed to load: {%s}.{%s}, {%s}", directory, file, e)
    logger.info("Loaded all cogs successfully.")


def init_bot(token, bot):
    try:
        load_cogs(bot)
        bot.run(token)
    except TypeError as e:
        print(e)


def main():
    args = parse_args()

    setup_logger(
        level=args.log_level if args.log_level else int(os.getenv("LOGGING_LEVEL", 20)),
        stream_logs=args.console_log if args.console_log != None else bool(os.getenv("STREAM_LOGS", False)),
    )

    bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
    bot.remove_command("help")

    if not args.drop_db:
        logger.info("Initialising Database...")
        initialise_bot_db(bot)

    server_settings_path = args.server_settings_path if args.server_settings_path else os.environ.get("SERVER_SETTINGS")
    if server_settings_path:
        logger.info(f"Loading server settings from {server_settings_path}")
        bot.server_settings = Settings(server_settings_path)  # type: ignore

    if args.discord_token:
        init_bot(args.discord_token, bot)
    else:
        init_bot(os.getenv("DISCORD_TOKEN"), bot)


if __name__ == "__main__":
    main()
