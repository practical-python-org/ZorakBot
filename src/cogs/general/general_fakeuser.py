"""
A simple command that gives back a fake user
"""
import logging
import json
import requests
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralFakeUser(commands.Cog):
    """
    # Hits the randomuser API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def fakeperson(self, ctx):
        """
        Sends a fake person using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        person = json.loads(
            requests.get(
                "https://randomuser.me/api/"
                , timeout=5).text)["results"]
        name = f'Name: {person[0]["name"]["title"]}' \
               f' {person[0]["name"]["first"]}' \
               f' {person[0]["name"]["last"]}'

        hometown = f'Hometown:' \
                   f' {person[0]["location"]["city"]},' \
                   f' {person[0]["location"]["country"]}'
        age = f'Age: {person[0]["dob"]["age"]} Years old'
        await ctx.respond(
            "You have requested a fake person:\n\n"
            + name
            + "\n"
            + hometown
            + "\n"
            + age
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralFakeUser(bot))
