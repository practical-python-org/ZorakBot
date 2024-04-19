"""
Admin command for kicking a user.
"""
import logging

import discord
from discord.ext import commands
from discord.utils import get

from zorak.utilities.cog_helpers._embeds import (
    embed_cant_do_that, embed_quarantine  # pylint: disable=E0401
)

logger = logging.getLogger(__name__)


class AdminQuarantine(commands.Cog):
    """
    Command to quarantine a user.
    """

    def __init__(self, bot):
        self.bot = bot
        self.message_counter = 0

    @commands.slash_command(description="Quarantine a user.")
    @commands.has_permissions(moderate_members=True)
    @commands.has_role("Staff")
    async def quarantine(self, ctx, target: discord.Member, number_of_messages_to_remove=0):
        """
        Take in a user mention, and an int amount of messages to remove.
        """
        # Cant ban bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:

                mod_log = await self.bot.fetch_channel(
                    self.bot.server_settings.log_channel["mod_log"])

                # TODO: Getting a None from roles. Will look tomorrow.
                verified_role = get(ctx.guild.roles, id=self.bot.server_settings.verified_role)
                naughty_role = get(ctx.guild.roles, id=self.bot.server_settings.badboi_role)

                await target.remove_roles(verified_role)
                await target.add_roles(naughty_role)
                logger.info(f"removed verified")
                logger.info(f"added naughty")

                # remove messages, if that was specified.
                if number_of_messages_to_remove > 0:
                    if number_of_messages_to_remove != self.message_counter:
                        for channel in ctx.guild.text_channels:
                            async for message in channel.history(limit=50):
                                if message.author.id == target.id:
                                    await message.delete()
                                    self.message_counter += 1

                await ctx.respond(f"Quarantined {target.name}.", ephemeral=True)
                await mod_log.send(embed=embed_quarantine(ctx.author, target, self.message_counter))


            else:
                await ctx.respond(embed=embed_cant_do_that("You can't quarantine an Admin."), ephemeral=True)
        else:
            await ctx.respond(embed=embed_cant_do_that("You cant quarantine a bot."), ephemeral=True)


def setup(bot):
    """
    required.
    """
    bot.add_cog(AdminQuarantine(bot))
