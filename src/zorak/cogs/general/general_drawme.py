"""
uses computerrender API to make a CGI image
"""
import logging
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralDrawMe(commands.Cog):
    """
    uses computerrender API to make a CGI image
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Generates an AI-made image from a prompt.")
    async def drawme(self, ctx, prompt, seed):
        """
        Sends a computer generated image based on a prompt.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        sanetized = prompt.replace(" ", "-")
        gen_url = f"https://api.computerender.com/generate/{sanetized}"
        if seed:
            gen_url = gen_url + f"?seed={seed}"
        embed = discord.Embed.from_dict(
            {"title": prompt, "color": 10848322, "image": {"url": gen_url}}
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralDrawMe(bot))
