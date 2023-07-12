"""
A simple taunt command.
"""
import logging
from bs4 import BeautifulSoup
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralTaunt(commands.Cog):
    """
    # Hits the fungenerators.com website, and scrapes the data there.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def taunt(self, ctx, person):
        """
        Scrapes a webpage for shakespearean taunts.
        """
        taunt = BeautifulSoup(
            requests.get(
                "https://fungenerators.com/random/insult/shakespeare/"
                , timeout=5
            ).content,
            "html.parser",
        ).find("h2")
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(f"{person}, {taunt.text}")


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralTaunt(bot))
