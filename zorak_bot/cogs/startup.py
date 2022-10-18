from discord.ext import commands

class onStartup(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Greetings, puny earth-creature.')

def setup(bot):
    bot.add_cog(onStartup(bot))