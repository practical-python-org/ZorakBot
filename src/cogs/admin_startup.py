from discord.ext import commands
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class onStartup(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Successfully logged in as {self.bot.user}/ ID: {self.bot.user.id}")
        logger.info(f"Started at: {datetime.now()}")
        print('Greetings, puny earth-creature.')

def setup(bot):
    bot.add_cog(onStartup(bot))