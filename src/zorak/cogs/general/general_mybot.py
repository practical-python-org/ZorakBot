"""
Generate a bot, monster, human, or cat for fun.
"""
import logging

import discord
from discord.ext import commands
from discord.commands import option

logger = logging.getLogger(__name__)


class MyBot(commands.Cog):
    """
    # Grabs png from https://robohash.org/.
    """

    def __init__(self, bot):
        self.bot = bot
        self.bot_types = ["Robot", "Monster", "Bot Head", "Cat", "Human"]

    async def get_type(self, ctx: discord.AutocompleteContext):
        """Helper function for the bot_type arg"""
        return [item for item in self.bot_types if item.startswith(ctx.value.upper())]


    @commands.slash_command(name="mybot")
    @option("seed", description="Enter any text to use as seed.")
    @option("bot_type", description="What type of robot?", autocomplete=get_type)
    async def mybot(self, ctx, *, seed="", bot_type="Robot"):
        """
        Sends a custom bot pic using an API
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)

        if bot_type in self.bot_types:
            n = self.bot_types.index(bot_type) + 1
        else:
            n = 1

        seed = seed or ctx.author.name

        url = f'https://robohash.org/{seed}?set=set{n}'
        embed = discord.Embed(title="Meet your bot!")
        embed.set_image(url=url)
        embed.set_footer(text="Robots lovingly delivered by Robohash.org")
        await ctx.respond(embed=embed)


def setup(bot):
    """
    Required.
    """
    bot.add_cog(MyBot(bot))