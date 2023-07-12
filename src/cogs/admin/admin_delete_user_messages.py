"""
Admin command for deleting a users historical messages
TODO: Finish this cog. It is currently named with a _ prefix so that it is not loaded.
"""
import logging
from datetime import datetime, timedelta
import time
import discord
from discord.ext import commands
from utilities.cog_helpers._embeds import embed_cant_do_that  # pylint: disable=E0401


logger = logging.getLogger(__name__)


class AdminDeleteMessages(commands.Cog):
    """
    Command to remove x messages by a user.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="Deletes all messages from a user over a timeperiod in minutes.")
    @commands.has_permissions(manage_messages=True)
    @commands.has_role("Staff")
    async def delete_messages(self, ctx, target: discord.Member, minutes):
        """
        Take in a user, and a timeperiod in minutes.
        """
        await ctx.defer(ephemeral=True)
        counter = 0
        time_ago = datetime.utcnow() - timedelta(minutes=int(minutes))

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                async for message in channel.history(limit=300, after=time_ago):
                    if message.author.id == target.id:
                        await message.delete()
                        time.sleep(.3)
                        counter += 1

        await ctx.followup.send(
            embed=embed_cant_do_that(
                f"{ctx.author.name} deleted {str(counter)} messages by {target.name}."))


def setup(bot):
    """
    required.
    """
    bot.add_cog(AdminDeleteMessages(bot))
