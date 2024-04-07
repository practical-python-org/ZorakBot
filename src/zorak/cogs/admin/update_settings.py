"""
A simple hello command.
"""
import logging
import discord
from discord import option
from discord.ext import commands

logger = logging.getLogger(__name__)


class Settings(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """

    def __init__(self, bot):
        self.bot = bot  # Passed in from main.py

    @commands.slash_command(description="See the bot settings for your guild!")
    async def setup_zorak(self, ctx):
        if not self.bot.db_client.guild_exists_in_db(ctx.guild):
            self.bot.db_client.add_guild_to_table(ctx.guild)
            await ctx.respond(
                f"## **Added {ctx.guild.name} to database.**"
                f"\n\nPlease use the **/update_roles** command to set Guild roles."
                f"\nPlease use the **/update_channels** command to set Guild channels."
                f"\nPlease use the **/update_logging_channels** command to set Guild log channels."
                f"\n\nTo see roles, use **/see_roles**."
                f"\nTo see channels, use **/see_channels**."
                f"\nTo see logging channels, use **/see_logging_channels**."
            )
        else:
            await ctx.respond(
                f"Looks like {ctx.guild.name} is already in the database."
                f"\n\nTo see roles, use **/see_roles**."
                f"\nTo see channels, use **/see_channels**."
                f"\nTo see logging channels, use **/see_logging_channels**."
            )


    ####################
    #  Roles
    ####################
    @commands.slash_command(description="See the roles for your guild!")
    async def see_roles(self, ctx):
        """The slash command that initiates the fancy menus."""
        settings = self.bot.db_client.get_guild_settings(ctx.guild)
        pretty_printed_settings = ""
        for key, value in settings.items():
            if "_role" in key:
                pretty_printed_settings += f"{key}: <@{value}>\n"

        await ctx.respond(f"### Guild Roles for {ctx.guild}\n{pretty_printed_settings}")

    @commands.slash_command()
    @option(
        "position"
        , description="All options for roles."
        , choices=[
            "Guild Owner role"
            , "Administrator role"
            , "Staff/Moderatior role"
            , "Networking role"
            , "Zorak's Bot role"
            , "Punishment/Quarantine role"
            , "Verification role"
        ])
    async def update_roles(
        self
        , ctx: discord.ApplicationContext
        , position: str
        , role: discord.Role
    ):
        mapper = {
            "Guild Owner role": "owner_role",
            "Administrator role": "admin_role",
            "Staff/Moderator role": "staff_role",
            "Networking role": "networking_role",
            "Zorak's Bot role": "bot_role",
            "Punishment/Quarantine role": "naughty_role",
            "Verification role": "verified_role"
        }
        self.bot.db_client.update_guild_settings(ctx.guild, mapper[position], int(role.id))
        logger.info(f"{ctx.author.name} updated {mapper[position]} in {ctx.guild.name} to {role.id}")
        await ctx.respond(f"Updated {position} in {ctx.guild.name}. New Value: {role.mention}")

    ####################
    #  Normal Channels
    ####################
    @commands.slash_command(description="See the channels for your guild!")
    async def see_channels(self, ctx):
        """The slash command that initiates the fancy menus."""
        settings = self.bot.db_client.get_guild_settings(ctx.guild)
        pretty_printed_settings = ""
        for key, value in settings.items():
            if "_channel" in key:
                pretty_printed_settings += f"{key}: <#{value}>\n"

        await ctx.respond(f"### Guild channels for {ctx.guild}\n{pretty_printed_settings}")

    @commands.slash_command()
    @option(
        "option"
        , description="All options for Guild channels."
        , choices=[
            "Verification Channel"
            , "Quarantine Channel"
            , "Support/Ticket Channel"
            , "Reaction Role Channel"
            , "Rules Channel"
            , "General Channel"
            , "Resources Channel"
            , "Challenges Channel"
        ])
    async def update_channels(
        self
        , ctx: discord.ApplicationContext
        , option: str
        , channel: discord.TextChannel
    ):
        mapper = {
            "Verification Channel": "verification_channel",
            "Quarantine Channel": "quarantine_channel",
            "Support/Ticket Channel": "support_channel",
            "Reaction Role Channel": "role_channel",
            "Rules Channel": "rules_channel",
            "General Channel": "general_channel",
            "Resources Channel": "resources_channel",
            "Challenges Channel": "challenges_channel"
        }
        self.bot.db_client.update_guild_settings(ctx.guild, mapper[option], int(channel.id))
        logger.info(f"{ctx.author.name} updated {mapper[option]} in {ctx.guild.name} to {channel.id}")
        await ctx.respond(f"Updated {option} in {ctx.guild.name}. New Value: {channel.mention}")

    ####################
    #  Logging Channels
    ####################

    @commands.slash_command(description="See the logging channels for your guild!")
    async def see_logging_channels(self, ctx):
        """The slash command that initiates the fancy menus."""
        settings = self.bot.db_client.get_guild_settings(ctx.guild)
        pretty_printed_settings = ""
        for key, value in settings.items():
            if "_log" in key:
                pretty_printed_settings += f"{key}: <#{value}>\n"

        await ctx.respond(f"### Guild logging channels for {ctx.guild}\n{pretty_printed_settings}")

    @commands.slash_command()
    @option(
        "logs"
        , description="All options for logging channels."
        , choices=[
            "User chat logs"
            , "Join/leave logs"
            , "Moderation action logs"
            , "Server change logs"
            , "User change logs"
            , "Verification logs"
            , "Zorak error logging"
        ])
    async def update_logging_channels(
        self
        , ctx: discord.ApplicationContext
        , logs: str
        , channel: discord.TextChannel
    ):
        mapper = {
            "User chat logs": "chat_log",
            "Join/leave logs": "join_log",
            "Moderation action logs": "mod_log",
            "Server change logs": "server_change_log",
            "User change logs": "user_log",
            "Verification logs": "verification_log",
            "Zorak error logging": "zorak_log"
        }
        self.bot.db_client.update_guild_settings(ctx.guild, mapper[logs], int(channel.id))
        logger.info(f"{ctx.author.name} updated {mapper[logs]} in {ctx.guild.name} to {channel.id}")
        await ctx.respond(f"Updated {logs} in {ctx.guild.name}. New Value: {channel.mention}")


def setup(bot):
    """
    Required.
    """
    bot.add_cog(Settings(bot))
