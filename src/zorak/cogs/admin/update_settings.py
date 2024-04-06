"""
A simple hello command.
"""
import logging
from random import shuffle
import discord
from discord.ext import commands
from time import sleep

logger = logging.getLogger(__name__)



class Settings(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """

    def __init__(self, bot):
        self.bot = bot  # Passed in from main.py

    @commands.slash_command(description="Edit the bot settings for your guild!")
    async def update_settings(self, ctx, setting: str, value: str):
        """The slash command that initiates the fancy menus."""
        self.bot.db_client.update_guild_settings(ctx.guild, setting, int(value))

        await ctx.respond(f"Updated {setting} in {ctx.guild.name}. New Value: {value}")




def setup(bot):
    """
    Required.
    """
    bot.add_cog(Settings(bot))
