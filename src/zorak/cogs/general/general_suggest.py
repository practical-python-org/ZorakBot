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
        
        '''
        
        '''
        embed = discord.Embed(description= question)
        embed.set_author(name= f"Suggestion by user {ctx.author.name}")
        error_embed = discord.Embed(title= "**Oops...**", description= "Slow down, please only use /suggest in #📎suggestions!", color= discord.Color.red())


        '''
        If the channel name/ID of the command matches with the current 
        channel, the suggestion will be posted. If not, an error message will occur.
        '''
        if ctx.channel.name == "📎suggestions" or ctx.channel_id == "962415552737996800":
            msg = await ctx.respond(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        else:
            await ctx.respond(embed=error_embed)


def setup(bot):
    """Required."""
    bot.add_cog(GeneralSuggest(bot))
