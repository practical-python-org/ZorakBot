"""
A simple dogfact command.
"""
import logging
import json
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralDogFact(commands.Cog):
    """
    # Hits the dogfact API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def dogfact(self, ctx):
        """
        Sends a dog fact using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(
            json.loads(
                requests.get(
                    "https://dog-api.kinduff.com/api/facts"
                    , timeout=5).text)["facts"][0]
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralDogFact(bot))
