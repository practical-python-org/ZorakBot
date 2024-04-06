"""
A command that retrieves a computer-generated image of a nonexistent person
"""

from io import BytesIO
import logging

import requests
from discord.ext import commands
from discord import File


logger = logging.getLogger(__name__)


class GeneralThisPersonDoesNotExist(commands.Cog):
    """
    Gets a randomly-provided image from 'thispersondoesnotexist.com'
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def thispersondoesnotexist(self, ctx):
        logger.info(f"{ctx.author.name} used the {ctx.command} command.")

        response = requests.get("https://thispersondoesnotexist.com/")
        with BytesIO() as image_binary:
            image_binary.write(response.content)
            image_binary.seek(0)
            await ctx.respond(content="This person does not exist.",
                              file=File(image_binary, "image.jpg"))


def setup(bot):
    """
    Required
    """

    bot.add_cog(GeneralThisPersonDoesNotExist(bot))
