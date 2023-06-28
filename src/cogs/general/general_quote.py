"""
A simple quote command.
"""
import logging
import json
import requests
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralQuote(commands.Cog):
    """
    # Hits the zenquotes API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def quote(self, ctx):
        """
        Sends a quote using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        quote = json.loads(
            requests.get(
                "https://zenquotes.io/api/random"
                , timeout=5).text)[0]
        await ctx.respond((quote["q"] + "\n- " + quote["a"]))


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralQuote(bot))
