import logging
import os
from datetime import datetime

import discord
from discord.ext import commands

from utilities.core.args_utils import parse_args
from utilities.core.logging_utils import setup_logger
from utilities.core.mongo import initialise_bot_db

logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
bot.remove_command("python")


def load_cogs(bot):
    cogs_directory = "/src/cogs"
    files = os.listdir(cogs_directory)
    for f in files:
        if f.endswith(".py") and not f.startswith("_"):
            cog = f[:-3]
            logger.info(f"Loading Cog: {cog}")
            bot.load_extension(f"cogs.{cog}")
    return bot


@bot.event
async def on_ready():
    logger.info(f"version: {discord.__version__}")
    logger.info(f"Successfully logged in as {bot.user}/ ID: {bot.user.id}")
    logger.info(f"Started at: {datetime.now()}")


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


if __name__ == "__main__":
    args = parse_args()
    setup_logger(
        level=int(os.getenv("LOGGING_LEVEL", 20)),
        stream_logs=bool(os.getenv("STREAM_LOGS", False)),
    )
    initialise_bot_db(bot)
    load_cogs(bot)
    try:
        bot.run(os.getenv("TOKEN"))
    except TypeError as e:
        print(e)
