"""
The in-house server bot of Practical Python!
- https://discord.gg/vgZmgNwuHw
- https://github.com/practical-python-org/ZorakBot
- Practicalpython-staff@pm.me
"""
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands

from utilities.core.logging_utils import setup_logger
from utilities.core.mongo import initialise_bot_db


logger = logging.getLogger(__name__)
setup_logger(
    level=int(os.getenv("LOGGING_LEVEL", 20)),
    stream_logs=bool(os.getenv("STREAM_LOGS", False)),
)

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
bot.remove_command("help")

for cog_path in Path("./cogs").glob("*.py"):
    cog_name = cog_path.stem
    DOTTED_PATH = "cogs.{cog_name}"
    if cog_name not in ('__init__', '_settings'):
        logger.info("loading... {%s}", DOTTED_PATH)
        try:
            bot.load_extension(str(DOTTED_PATH))
        except Exception as e:
            logger.info("Failed to load cog {%s} - exception:{%s}", DOTTED_PATH, e)
        logger.info("loaded {%s}", DOTTED_PATH)


@bot.listen("on_interaction")
async def log_interaction(interaction):
    """
    This logs all interactions used by anyone, and logs them.
    """
    if interaction is not None:
        logger.info("requester: {%s}",str(interaction.user))
        logger.info("Command: {%s}", str(interaction.data))


@bot.listen("on_message")
async def log_message(message):
    """
    This logs all commands used by anyone in the server.
    """
    if message.interaction is not None:
        logger.info("response: {%s}", str(message.content))
        # logger.info(f"url: {str(message.jump_url)}")


initialise_bot_db(bot)
try:
    bot.run(os.getenv("DISCORD_TOKEN"))
except TypeError as e:
    print(e)
