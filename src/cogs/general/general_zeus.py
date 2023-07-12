"""
Checks if a website is online
"""
import logging
import requests
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralZeus(commands.Cog):
    """Checks if a website is online"""
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Checks a URL to see if its online.")
    async def zeus(self, ctx, url):
        """
        Checks if a website is currently Up and reachable.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        if "https://" in url:
            try:
                requests.get(url=url, timeout=2.5, verify=False)
                context = (url, "**ONLINE**")
            except requests.exceptions.ConnectionError:
                context = (url, "**OFFLINE**")
        else:
            fix_url = f"https://{url}"
            try:
                requests.get(url=fix_url, timeout=2.5, verify=False)
                context = (fix_url, "**ONLINE**")
            except requests.exceptions.ConnectionError:
                context = ("INVALID URL", "Please try again")

        if context[1] == "**ONLINE**":
            color = discord.Color.green()
        else:
            color = discord.Color.red()
        embed = discord.Embed(title="ZeusTheInvestigator", description="", color=color)
        embed.add_field(
            name=f"Checked link: *{context[0]}*", value=f"STATUS: {context[1]}"
        )
        embed.set_footer(text="Credits to: @777advait#6334")
        await ctx.respond(embed=embed)


def setup(bot):
    """Required."""
    bot.add_cog(GeneralZeus(bot))
