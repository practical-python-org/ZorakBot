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
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def docs(self, ctx, searchterm):

        r = requests.get('https://docs.python.org/3/genindex-all.html')
        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all('a')
        title = soup.find_all('title')
        version = title[0].text.split('—')[1].strip()

        results = []
        for i in links:
            if searchterm in i['href']:
                results.append(f"https://docs.python.org/3/{i['href']}")

        embed = embed_docs(searchterm, version, results)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Documentation(bot))
