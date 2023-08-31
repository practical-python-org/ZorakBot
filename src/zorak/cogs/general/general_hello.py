"""
A simple hello command.
"""
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralHello(commands.Cog):
    """
    # This cog can be used as a template for any command.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def hello(self, ctx):
        """
        A simple hello.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond("Don't talk to me, I am being developed!")


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralHello(bot))
