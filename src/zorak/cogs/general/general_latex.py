"""
LaTeX command to generate mathematical equations.
"""
import logging

import discord
import requests
import json

from discord.ext import commands
from discord.commands import Option
from pathlib import Path


logger = logging.getLogger(__name__)

class LaTeX(commands.Cog):
    """
    # Grabs the svg code from codecogs API and converts it to a png for display in an embed.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def latex_bg(self, ctx):
        embed = discord.Embed(title="LaTeX Background Colors", description="The following colors are available:")
        file = discord.File(Path.cwd().joinpath("src", "zorak", "utilities", "cog_helpers", "bg_colors.png"), filename="bg_colors.png")
        embed.set_image(url="attachment://bg_colors.png")
        await ctx.respond(file=file, embed=embed, ephemeral=True)
    
    @commands.slash_command()
    async def latex_txt(self, ctx):
        embed = discord.Embed(title="LaTeX Background Colors", description="The following colors are available:")
        file = discord.File(Path.cwd().joinpath("src", "zorak", "utilities", "cog_helpers", "txt_colors.png"), filename="txt_colors.png")
        embed.set_image(url="attachment://txt_colors.png")
        await ctx.respond(file=file, embed=embed, ephemeral=True)

    @commands.slash_command()
    async def latex(self, ctx, 
        equation: Option(str, "LaTeX equation ($ on both ends not needed)", required = True, default = ""), 
        *, 
        bg_color: Option(str, "Use '/latex_bg' to see available colors.", required = False, default = "black"), 
        txt_color: Option(str, "Use '/latex_txt' to see available colors.", required = False, default = "White"), 
        dpi: Option(int, "Choose an image size (default: 200)", required = False, default = 200)
        ):
        """
        Send a mathematical equation using LaTeX commands

        Parameters:
            equation (str): The mathematical equation to render using LaTeX.
            bg_color (str, optional): Background color for the LaTeX image. Use '/latex_bg' to see available colors. Default is "black".
            txt_color (str, optional): Text color for the LaTeX image. Use '/latex_txt' to see available colors. Default is "White".
            dpi (int, optional): Choose an image size (default: 200).
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        
        # check for valid user specified color for text and background
        with open(Path.cwd().joinpath("src", "zorak", "utilities", "cog_helpers", "colors.json")) as f:
            d = json.load(f)
        bg_colors = d["bg_colors"]
        txt_colors = d["txt_colors"]

        bg_color = bg_color.lower().replace(" ", "")
        txt_color = txt_color.title().replace(" ", "")

        if bg_color not in bg_colors:
            bg_color = "black"
        if txt_color not in txt_colors:
            txt_color = "White"

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
            await ctx.respond("Failed to fetch the image from the API", ephemeral=True)
        

def setup(bot):
    """
    Required.
    """
    bot.add_cog(LaTeX(bot))