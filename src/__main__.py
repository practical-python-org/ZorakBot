"""
The in-house server bot of Practical Python!
- https://discord.gg/vgZmgNwuHw
- https://github.com/practical-python-org/ZorakBot
- Practicalpython-staff@pm.me
"""
import logging
import os
import sys
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


def load_cogs():
    """
    Loads the directories under the /cogs/ folder,
    then digs through those directories and loads the cogs.
    """
    logger.info("Loading Cogs...")
    for directory in os.listdir("./cogs"):
        if not directory.startswith("_"):  # Makes sure __innit.py__ doesnt get called
            for file in os.listdir(f"./cogs/{directory}"):
                if file.endswith('.py') and not file.startswith("_"):
                    try:
                        logger.info(f"Loading Cog: \\{directory}\\{file}")
                        bot.load_extension(f"cogs.{directory}.{file[:-3]}")
                    except Exception as e:
                        logger.critical("Failed to load: {%s}.{%s}, {%s}", directory, file, e)
    logger.info("Loaded all cogs successfully.")


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
    load_cogs()
    bot.run(os.getenv("DISCORD_TOKEN"))
except TypeError as e:
    print(e)
