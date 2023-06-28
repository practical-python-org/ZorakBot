"""
A simple pugfact command.
"""
import logging
from bs4 import BeautifulSoup
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralPugFact(commands.Cog):
    """
    # Hits the pugfact API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def pugfact(self, ctx):
        """
        Sends a pug fact using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(
            BeautifulSoup(
                requests.get(
                    "https://fungenerators.com/random/facts/dogs/pug"
                    , timeout=5).content
                , "html.parser")
            .find("h2")
            .text[:-15]
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralPugFact(bot))
