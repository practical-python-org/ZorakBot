"""
Ping
"""
import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class Ping(commands.Cog):
    """Ping command"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """It's a me, a ping command."""

        if message.content.startswith('!ping'):
            logger.info("%s used a ping command."
                        , message.author.name)
            await message.channel.send(f'Ping: {round(self.bot.latency, 3)}ms')
            return


def setup(bot):
    """Required."""
    bot.add_cog(Ping(bot))
