import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from io import BytesIO
import datetime
import json
import logging
import pytz
import requests

requests.packages.urllib3.disable_warnings()

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(FunCog(bot))
