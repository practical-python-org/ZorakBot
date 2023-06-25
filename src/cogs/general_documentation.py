"""
Grabs the selected item from the Python documentation
"""
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import logging

from utilities.cog_helpers._embeds import embed_docs


logger = logging.getLogger(__name__)


class Documentation(commands.Cog):
    """
    This allows us to search the Python docs for things.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def docs(self, ctx, searchterm):
        """
        We use Overapi to search, as it weeds out a lot of the
        noise from the documentation.
        For now, this covers all basic methods and functions.
        """
        soup = BeautifulSoup(
            requests.get('https://overapi.com/python').content
            , 'html.parser'
        )
        links = soup.find_all('a')
        search_results = []

        for i in links:
            if 'http://docs.python.org' in str(i) and searchterm in str(i['href']):
                name = i['href'].split('.')[-1]
                link = i['href']
                description = i['title']
                result = tuple((name, link, description))
                search_results.append(result)

        embed = embed_docs(searchterm, search_results)

        await ctx.respond(embed=embed)


def setup(bot):
    """
    dOcStRiNgS aRe GrEaT...
    """
    bot.add_cog(Documentation(bot))
