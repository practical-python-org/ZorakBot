"""
Uses boredAPI to send a "interesting" thing to do.
"""
import logging
import requests
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralBored(commands.Cog):
    """
    Uses boredAPI to send a "interesting" thing to do.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Gives you something to do.")
    async def imbored(self, ctx):
        """
        Sends a "thing-to-do using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        data = requests.get(
            "https://www.boredapi.com/api/activity/"
            , timeout=5).json()
        if data["price"] < 0.5:
            price = "and is not too expensive"
        else:
            price = "and is a bit expensive"
        await ctx.respond(
            f'Im bored too...\nLets do this: {data["activity"]}.'
            f'\nIts {data["type"]} and you could involve '
            f'{str(data["participants"])} people {price}'
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralBored(bot))
