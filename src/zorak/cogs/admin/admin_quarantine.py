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


class AdminQuarantine(commands.Cog):
    """
    Command to ban a user. Takes in a name, and a reason.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Quarantine a user.")
    @commands.has_permissions(manage_roles=True)
    @commands.has_role("Staff")
    async def quarantine(self, ctx, target: discord.Member):
        """
        Take in a user mention, and a string reason.
        """
        # Cant ban bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:
                quarantine_role = discord.utils.get(ctx.guild.roles, id=self.bot.user_roles.badboi_role["naughty"])
                await target.edit(roles=[quarantine_role])

                logger.info("{%s} quarantined {%s}.", ctx.author.name, target.name)

            else:
                await ctx.respond(embed=embed_cant_do_that("You can't quarantine an Admin."), ephemeral=True)
        else:
            await ctx.respond(embed=embed_cant_do_that("You cant quarantine a bot."), ephemeral=True)


def setup(bot):
    """
    required.
    """
    bot.add_cog(AdminQuarantine(bot))
