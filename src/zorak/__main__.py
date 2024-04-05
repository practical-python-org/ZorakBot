"""
The in-house server bot of Practical Python!
- https://discord.gg/vgZmgNwuHw
- https://github.com/practical-python-org/ZorakBot
- Practicalpython-staff@pm.me
"""
import logging
from datetime import datetime
import os

import discord
from discord.ext import commands

from zorak.utilities.core.args_utils import parse_args
from zorak.utilities.core.logging_options import setup_logger
from zorak.utilities.core.mongo import initialise_bot_db
from zorak.utilities.core.settings import Settings


logger = logging.getLogger(__name__)

server_settings_path = None


def load_cogs(bot):
    """
    Loads the directories under the /cogs/ folder,
    then digs through those directories and loads the cogs.
    """
    COGS_ROOT_PATH = os.path.join(os.path.dirname(__file__), "cogs")
    logger.info("Loading Cogs...")
    logger.info(f"Loading from {COGS_ROOT_PATH}")
    failed_to_load = []
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
                try:
                    bot.load_extension(f"zorak.cogs.{directory}.{file[:-3]}")
                    logger.debug(f"Loaded Cog: {cog_path}")
                except Exception as e:
                    logger.warning("Failed to load: {%s}.{%s}, {%s}", directory, file, e)
                    failed_to_load.append(f"{file[:-3]}")
    if failed_to_load:
        logger.warning(f"Cog loading finished. Failed to load the following cogs: {', '.join(failed_to_load)}")
    else:
        logger.info("Loaded all cogs successfully.")


def init_bot(token, bot):
    try:
        load_cogs(bot)
        bot.run(token)

    except TypeError as e:
        print(e)



def main():
    args = parse_args()

    bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
    bot.remove_command("help")


    # Set up global logging across the bot.
    setup_logger(
        level=args.log_level if args.log_level else int(os.getenv("LOGGING_LEVEL", 20)),
        stream_logs=args.console_log if args.console_log != None else bool(os.getenv("STREAM_LOGS", False)),
    )
    if not args.drop_db:
        logger.info("Initialising Database...")
        initialise_bot_db(bot)

    settings_path = args.server_settings_path if args.server_settings_path else os.environ.get(
        "SERVER_SETTINGS")

    if settings_path:
        logger.info(f"Loading all server settings from {settings_path}")
        bot.settings = Settings(settings_path, bot.guilds)  # type: ignore

    if args.discord_token:
        init_bot(args.discord_token, bot)
    else:
        init_bot(os.getenv("DISCORD_TOKEN"), bot)


if __name__ == "__main__":
    main()
