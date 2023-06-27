"""
Ping
"""
from discord.ext import commands


class Ping(commands.Cog):
    """Ping command"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """It's a me, a ping command."""
        if message.content.startswith('!ping'):
            await message.channel.send(f'Ping: {round(self.bot.latency, 3)}ms')
            return


def setup(bot):
    """Required."""
    bot.add_cog(Ping(bot))
