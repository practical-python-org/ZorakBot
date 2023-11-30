"""
Adds an embed question, with a thumbsup and thumbsdown emoji
for voting on things.
"""
import logging
import discord
from discord.ext import commands


from zorak.utilities.cog_helpers._embeds import embed_suggestions, embed_suggestion_error  # pylint: disable=E0401


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
        If the channel name/ID of the command matches with the current
        channel, the suggestion will be posted. If not, an error message will occur.
        '''
        suggest_channel = await self.bot.fetch_channel(self.bot.server_settings.normal_channel["suggestions_channel"])
        if ctx.channel_id == suggest_channel.id:
            await ctx.response.send_message(embed=embed_suggestions(ctx.author, question))
            msg = await ctx.interaction.original_response()

            await msg.add_reaction(emoji="👍")
            await msg.add_reaction(emoji="👎")

        else:
            await ctx.respond(embed=embed_suggestion_error(suggest_channel))


def setup(bot):
    """Required."""
    bot.add_cog(GeneralSuggest(bot))
