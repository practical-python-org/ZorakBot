"""
A simple joke command.
"""
import logging
import json
import requests
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralJoke(commands.Cog):
    """
    # Hits the geek-jokes API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def joke(self, ctx):
        """
        Sends a joke using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(
            json.loads(
                requests.get(
                    "https://geek-jokes.sameerkumar.website/api?format=json"
                    , timeout=5).text)["joke"])


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralJoke(bot))
