from discord.ext import commands
from ._settings import log_channel


class LoggingRoles(commands.Cog):
    """
    Simple listener to on_member_update
    """
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        On member update, check if the roles changes, and then report what changed.
        logs_channel = await self.bot.fetch_channel(log_channel["user_log"])  # user join logs

        for role in before.roles:
            if role is not in after.roles:
                await logs_channel.send(f"{after.name} removed the <@{role}> role.")

        for role in after.roles:
            if role is not in before.roles:
                await logs_channel.send(f"{after.name} added the <@{role}> role.")

def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingRoles(bot))
