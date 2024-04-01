"""
Called upon startup of our bot.
Just logs some info. Nothing really.
"""
import os
import json
import logging
from datetime import datetime

from discord.ext import commands
from zorak.utilities.core.args_utils import parse_args

logger = logging.getLogger(__name__)


class OnStartup(commands.Cog):
    """
    onStartup is called when the bot reaches a stable state.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Here's the juice. It's literally logging.
        """
        logger.info("Successfully logged in as {%s}/ ID: {%s}", self.bot.user, self.bot.user.id)
        logger.info("Started at: {%s}", datetime.now())
        logger.info("Greetings, puny earth-creature.")

        # logger.info("---------------------------------")
        # logger.critical(self.bot.settings.server)
        # logger.info("---------------------------------")

def setup(bot):
    """
    required.
    """
    bot.add_cog(OnStartup(bot))
