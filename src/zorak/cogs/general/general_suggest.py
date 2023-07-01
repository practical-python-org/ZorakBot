"""
Adds an embed question, with a thumbsup and thumbsdown emoji
for voting on things.
"""
import logging
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralSuggest(commands.Cog):
    """
    Adds an embed question, with a thumbsup and thumbsdown emoji
    for voting on things.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def suggest(self, ctx, question):
        """
        Adds an embed question, with a thumbsup and thumbsdown emoji
        for voting on things.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        embed = discord.Embed(description=question)
        embed.set_author(name=f"Suggestion by {ctx.author.name}")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


def setup(bot):
    """Required."""
    bot.add_cog(GeneralSuggest(bot))
