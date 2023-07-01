"""
A simple catfact command.
"""
import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Debug(commands.Cog):
    """ """

    def __init__(self, bot):
        self.bot = bot
        logger.info("Loaded Debug Cog.")

    @commands.Cog.listener("on_interaction")
    async def log_interaction(interaction):
        """
        This logs all interactions used by anyone, and logs them.
        """
        if interaction is not None:
            logger.debug("requester: {%s}", str(interaction.user))
            logger.debug("Command: {%s}", str(interaction.data))

    @commands.Cog.listener("on_message")
    async def log_message(message):
        """
        This logs all commands used by anyone in the server.
        """
        if message.interaction is not None:
            logger.info("response: {%s}", str(message.content))
            # logger.info(f"url: {str(message.jump_url)}")


def setup(bot):
    """
    Required.
    """
    bot.add_cog(Debug(bot))
