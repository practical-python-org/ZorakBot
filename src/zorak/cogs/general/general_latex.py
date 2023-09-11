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
    async def latex(self, ctx, equation, *, bg_color = "black", txt_color = "white", dpi = 200):
        """
        Sends a mathematical equation using an API and CairoSVG
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        
        # check for valid user specified color for text and background
        colors = [
            #bg and txt ok
            "black", "white", "red", "yellow", "green", "blue", "cyan", "magenta", 
            #only bg ok
            "orange", "olive", "lime", "teal", "purple", "violet", "pink", "brown", "gray", "lightgray"
        ]

        bg_color = bg_color.replace(" ", "").lower()
        txt_color = txt_color.lower()

        if bg_color not in colors:
            bg_color = "black"
        if txt_color not in colors[:8]:
            txt_color = "white"

        # handle necessary character replacements
        escape_characters = {
            "\n": r"\n", "\r": r"\r", 
            "\t": r"\t", "\x08": r"\b", 
            "\x0c": r"\f", "\x0b": r"\v", 
            "\x07": r"\a", " ": "&space;"
        }

        for e, c in escape_characters.items():
            equation = equation.replace(e, c)

        # prevent user specified dpi from being too big
        dpi = max(int(dpi), 500)

        image_path = r"https://latex.codecogs.com/png.image?\dpi{" + f"{dpi}" + \
                    r"}\bg{" + bg_color + r"}\color{" + txt_color + "}" + equation

        r = requests.get(image_path, timeout=5)

        if r.status_code == 200:

            embed = discord.Embed(title="LaTeX", description=equation.replace("&space;", " "))
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