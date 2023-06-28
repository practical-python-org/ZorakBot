"""
A simple dog pic command.
"""
import logging
import requests
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralDogPic(commands.Cog):
    """
    # Hits the dog pic API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def dogpic(self, ctx, *, breed=None):
        """
        Sends a dog pic using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        embed = discord.Embed(
            title="Dog Pic!", description="A lovely dog pic just for you."
        )
        if breed is None:
            link = requests.get(
                "https://dog.ceo/api/breeds/image/random"
                , timeout=5).json()["message"]
        elif breed is not None:
            link = requests.get(
                f"https://dog.ceo/api/breed/{breed}/images/random"
                , timeout=5).json()["message"]
        embed.set_image(url=link)
        await ctx.respond(embed=embed)


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralDogPic(bot))
