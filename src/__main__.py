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
bot.remove_command("python")

for cog_path in Path("./cogs").glob("*.py"):
    cog_name = cog_path.stem
    dotted_path = f"cogs.{cog_name}"
    if cog_name != "__init__" and cog_name != "_settings":
        logger.info(f"loading... {dotted_path}")
        try:
            bot.load_extension(str(dotted_path))
        except Exception as e:
            logger.info(f"Failed to load cog {dotted_path} - exception:{e}")
        logger.info(f"loaded {dotted_path}")


@bot.listen("on_interaction")
async def log_interaction(interaction):
    if interaction is not None:
        logger.info(f"requester: {str(interaction.user)}")
        logger.info(f"Command: {str(interaction.data)}")


@bot.listen("on_message")
async def log_message(message):
    if message.interaction is not None:
        logger.info(f"response: {str(message.content)}")
        logger.info(f"url: {str(message.jump_url)}")


initialise_bot_db(bot)
try:
    bot.run(os.getenv("TOKEN"))
except TypeError as e:
    print(e)
