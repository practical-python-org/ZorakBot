"""
A simple catfact command.
"""
import logging
import json
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralCatFact(commands.Cog):
    """
    # Hits the catfact API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def catfact(self, ctx):
        """
        Sends a cat fact using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(
            json.loads(
                requests.get(
                    "https://catfact.ninja/fact"
                    , timeout=5).text)["fact"]
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralCatFact(bot))
