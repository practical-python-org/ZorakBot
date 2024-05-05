"""
Admin command for syncing guild commands
"""
import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class AdminSync(commands.Cog):
    """
    Two commands for syncing. Individual guild syncs and global syncs
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description="Sync all commands, in all guilds with Discord API")
    async def sync(self, ctx):

        message = f"{ctx.author.name} synced all commands for all guilds."
        logger.info("---- Attempting sync of all guilds")
        await self.bot.sync_commands(guild_ids=[])
        await ctx.respond(message)
        logger.info(message)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description="Sync the current guild's commands with Discord API")
    async def sync_guild(self, ctx):

        message = f"{ctx.author.name} synced all commands in {ctx.guild.name}."
        logger.info(f"---- Attempting sync of {ctx.guild.name}")
        await self.bot.sync_commands(guild_ids=[ctx.guild.id])
        await ctx.respond(message)
        logger.info(message)


    async def cog_command_error(
        self
        , ctx: commands.Context
        , error: commands.CommandError
    ):
        """
        Error handling for the entire Admin Cog
        """

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"Sorry, {ctx.author.name}, you dont have permission to use this command!",
                reference=ctx.message,
            )
        else:
            raise error


def setup(bot):
    """
    required.
    """
    bot.add_cog(AdminSync(bot))
