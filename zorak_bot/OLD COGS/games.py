from random import choice
from discord.ext import commands

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(GamesCog(bot))
