"""
Admin command for kicking a user.
"""
import logging

import discord
from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import (
    embed_cant_do_that,  # pylint: disable=E0401
)

logger = logging.getLogger(__name__)


class AdminBan(commands.Cog):
    """
    Command to ban a user. Takes in a name, and a reason.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ban a user.")
    @commands.has_permissions(ban_members=True)
    async def ban_member(self, ctx, target: discord.Member, reason):
        """
        Take in a user mention, and a string reason.
        """
        # Cant ban bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:
                # Message the user, informing them of their fate
                await target.send(
                    f"## You were banned by {ctx.author.name}.\n"
                    f"**Reason:** {reason}\n"
                    "\nIf you wish to appeal this ban,"
                    " contact PracticalPythonStaff@gmail.com"
                )
                # Then we do the ban
                await target.ban(reason=f"{ctx.author.name} - {reason}")
                logger.info("{%s} banned {%s}. Reason: {%s}", ctx.author.name, target.name, reason)
                # Then we publicly announce what happened.
                await ctx.respond(
                    embed=embed_cant_do_that(f"**{ctx.author.name}** banned **{target.name}**" f"\n"
                                             f"**Reason:** {reason}"))

            else:
                await ctx.respond(embed=embed_cant_do_that("You can't ban an Admin."), ephemeral=True)
        else:
            await ctx.respond(embed=embed_cant_do_that("You cant ban a bot."), ephemeral=True)


def setup(bot):
    """
    required.
    """
    bot.add_cog(AdminBan(bot))
