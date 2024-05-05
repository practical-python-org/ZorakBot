"""
A simple roll dice command
"""
from random import choice
import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralRollDice(commands.Cog):
    """
    # Rolls a 6 sided die.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def rolldice(self, ctx):
        """
        rolls a die.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(f"**{ctx.author.name}** rolled a **{choice(range(1, 7))}**")


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralRollDice(bot))
