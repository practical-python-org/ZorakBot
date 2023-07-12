"""
Logs when a member is UN-banned.
"""
from discord.ext import commands
from utilities.cog_helpers._embeds import embed_unban  # pylint: disable=E0401
from cogs._settings import log_channel  # pylint: disable=E0401


class LoggingUnbans(commands.Cog):
    """
    Simple listener to on_member_unban
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_unban(self, member):
        """
        Just listen for the event, embed it, and send it off.
        """
        embed = embed_unban(member)

        logs_channel = await self.bot.fetch_channel(log_channel['mod_log'])
        await logs_channel.send(embed=embed)


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingUnbans(bot))
