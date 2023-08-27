"""
Searches pypi for a package
"""
import logging
import requests
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class PipSearch(commands.Cog):
    """Searches pypi for a package"""
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Search Py-pi for a package.")
    async def pip_search(self, ctx, package):
        """
        Searches Pypi for a specific package.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        data = requests.get(f"https://pypi.org/pypi/{package}/json"
                            , timeout=5).json()
        try:
            embed = discord.Embed(
                title=f"Searched {package}",
                description=f"[Project URL]({data['info']['package_url']})",
                colour=discord.Colour.green(),
            )
            embed.add_field(
                name=f"{data['info']['name']} version {data['info']['version']}",
                value=f"{data['info']['summary']}",
            )
            await ctx.respond(embed=embed)

        except ValueError:
            await ctx.respond(
                embed=discord.Embed(
                    title="Oops...",
                    description="Invalid package name - " + package,
                    colour=discord.Colour.red(),
                )
            )


def setup(bot):
    """Required."""
    bot.add_cog(PipSearch(bot))
