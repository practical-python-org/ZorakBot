"""
A simple dadjoke command.
"""
import logging
import json
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralDadJoke(commands.Cog):
    """
    # Hits the icanhazdadjoke API and returns the response
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def dadjoke(self, ctx):
        """
        Sends a dad joke using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(
            json.loads(
                requests.get(
                "https://icanhazdadjoke.com/"
                , timeout = 5
                , headers = {"Accept": "application/json"}).text)["joke"]
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralDadJoke(bot))
