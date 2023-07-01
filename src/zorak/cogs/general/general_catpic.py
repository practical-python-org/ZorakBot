"""
A simple Cat pic command.
"""
import logging
from io import BytesIO
import requests
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralCatPic(commands.Cog):
    """
    # Hits the cat pic API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def catpic(self, ctx):
        """
        Sends a cat pic using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(
            file=discord.File(
                fp=BytesIO(
                    requests.get(
                        "https://cataas.com/cat"
                        , timeout=5).content),
                filename="cat.png",
            )
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralCatPic(bot))
