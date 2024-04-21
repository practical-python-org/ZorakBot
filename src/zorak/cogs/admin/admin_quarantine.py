"""
Admin command for kicking a user.
"""
import time
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
                message_counter = 0
                number_messages = int(number_of_messages_to_remove)

                mod_log = await self.bot.fetch_channel(
                    self.bot.server_settings.log_channel["mod_log"])

                # TODO: Getting a None from roles. Will look tomorrow.
                verified_role = get(ctx.guild.roles, id=self.bot.server_settings.verified_role['verified'])
                naughty_role = get(ctx.guild.roles, id=self.bot.server_settings.badboi_role['naughty'])

                try:
                    await target.remove_roles(verified_role)
                    await target.add_roles(naughty_role)
                    await ctx.respond(f"Quarantining {target.name}...", ephemeral=True)

                except Exception as notification1:
                    await ctx.respond("There was an issue with the command.", ephemeral=True)
                    logger.critical(f"There was an error in the Quarantine command...\n{notification1}")

                    # remove messages, if that was specified.
                    await ctx.send_followup(content=f"Removing {number_messages} messages by {target.name}...",
                                            ephemeral=True)

                    await ctx.defer()  # Necessary, as this process may take a bit.

                if number_messages != 0:
                    async for message in ctx.channel.history(limit=50):
                        if int(number_of_messages_to_remove) > message_counter:
                            if message.author.name == target.name:
                                await message.delete()
                                message_counter += 1
                                time.sleep(.2)  # Avoiding rate limits.

                await ctx.send_followup(
                    content=f"{target.name} has been quarantined, and {number_messages} messages have been removed.",
                    ephemeral=True)
                await mod_log.send(embed=embed_quarantine(ctx.author, target, message_counter))

            else:
                await ctx.respond(embed=embed_cant_do_that("You can't quarantine an Admin."), ephemeral=True)
        else:
            await ctx.respond(embed=embed_cant_do_that("You cant quarantine a bot."), ephemeral=True)

    @commands.slash_command(description="Release a user from quarantine.")
    @commands.has_permissions(moderate_members=True)
    @commands.has_role("Staff")
    async def unquarantine(self, ctx, target: discord.Member):
        if not target.bot:
            if not target.guild_permissions.administrator:

                mod_log = await self.bot.fetch_channel(
                    self.bot.server_settings.log_channel["mod_log"])

                verified_role = get(ctx.guild.roles, id=self.bot.server_settings.verified_role['verified'])
                naughty_role = get(ctx.guild.roles, id=self.bot.server_settings.badboi_role['naughty'])

                try:
                    await target.add_roles(verified_role)
                    await target.remove_roles(naughty_role)
                    await ctx.respond(f"Released {target.name} from quarantine", ephemeral=True)

                except Exception as notification1:
                    await ctx.respond("There was an issue with the command.", ephemeral=True)
                    logger.critical(f"There was an error in the unquarantine command...\n{notification1}")


def setup(bot):
    """
    required.
    """
    bot.add_cog(AdminQuarantine(bot))
