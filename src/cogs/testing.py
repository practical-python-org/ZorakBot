from discord.ext import commands


class Ping(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('!ping'):
            await message.channel.send(f'Ping: {round(self.bot.latency, 3)}ms')
            return


def setup(bot):
    bot.add_cog(Ping(bot))
