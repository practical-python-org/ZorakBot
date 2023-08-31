"""
Sends the Current local time of the moderation staff.\
"""
import logging
import datetime
import pytz
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class GeneralDevtimes(commands.Cog):
    """
    Sends the Current local time of the moderation staff.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Current times of Staff.")
    async def devtimes(self, ctx):
        """
        Sends the Current local time of the moderation staff.
        TODO: again, dict mapping could be good to help here,
            could also provide a command with timezone as input.
             Could do a whole times cog probably.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        tz_india = datetime.datetime.now(tz=pytz.timezone("Asia/Kolkata"))
        tz_japan = datetime.datetime.now(tz=pytz.timezone("Asia/Tokyo"))
        tz_america_ny = datetime.datetime.now(tz=pytz.timezone("America/New_York"))
        tz_austria = datetime.datetime.now(tz=pytz.timezone("Europe/Vienna"))
        tz_uk = datetime.datetime.now(tz=pytz.timezone("GMT"))

        embed = discord.Embed(title="**Staff Times**", description="")
        embed.add_field(
            name="Austria (Xarlos):",
            value=f"{tz_austria.strftime('%m/%d/%Y %I:%M %p')}",
            inline=False,
        )
        embed.add_field(
            name="Japan (Chiaki): ",
            value=f"{tz_japan.strftime('%m/%d/%Y %I:%M %p')}",
            inline=False,
        )
        embed.add_field(
            name="India (777advait):",
            value=f"{tz_india.strftime('%m/%d/%Y %I:%M %p')}",
            inline=False,
        )
        embed.add_field(
            name="America (Minus, Richardphi):",
            value=f"{tz_america_ny.strftime('%m/%d/%Y %I:%M %p')}",
            inline=False,
        )
        embed.add_field(
            name="UK (Maszi):",
            value=f"{tz_uk.strftime('%m/%d/%Y %I:%M %p')}",
            inline=False,
        )
        await ctx.respond(embed=embed)


def setup(bot):
    """Required."""
    bot.add_cog(GeneralDevtimes(bot))
