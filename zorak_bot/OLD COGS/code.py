import discord
import requests
from discord.ext import commands

class CodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(CodeCog(bot))
