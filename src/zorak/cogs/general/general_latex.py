"""
LaTeX command to generate mathematical equations.
"""
import logging

import discord
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)

class LaTeX(commands.Cog):
    """
    # Grabs the svg code from codecogs API and converts it to a png for display in an embed.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def latex(self, ctx, equation):
        """
        Sends a mathematical equation using an API and CairoSVG
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        escape_characters = {"\n": r"\n", "\r": r"\r", "\t": r"\t", "\x08": r"\b", "\x0c": r"\f", "\x0b": r"\v", "\x07": r"\a"}

        for e, c in escape_characters.items():
            equation = equation.replace(e, c)

        if " " in equation:  # The URL errors when it contains spaces.
            await ctx.respond("Your equation may not contain spaces!")
            return

        image_path = r"https://latex.codecogs.com/png.image?\dpi{200}\bg{black}\color{white}" + equation
        r = requests.get(image_path, timeout=5)

        if r.status_code == 200:

            embed = discord.Embed(title="LaTeX", description=equation)
            embed.set_image(url=image_path)  # Set the image in the embed

            # Send the embed with the image
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Failed to fetch the image from the API")
        



def setup(bot):
    """
    Required.
    """
    bot.add_cog(LaTeX(bot))