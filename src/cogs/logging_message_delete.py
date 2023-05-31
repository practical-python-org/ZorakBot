from discord.ext import commands
from ._settings import log_channel, server_info
from utilities.cog_helpers._embeds import  embed_message_delete


class LoggingMessageDelete(commands.Cog):
    """
    Simple listener to on_message_delete
    then checks the audit log for exact details
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        then we grab the guild, and from there read the last entry in the audit log.
        """
        current_guild = self.bot.get_guild(server_info['id'])
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == 'AuditLogAction.message_delete':
            member = current_guild.get_member(audit_log.user.id)

            embed = embed_message_delete(member, audit_log.target, message)

            logs_channel = await self.bot.fetch_channel(log_channel["chat_log"])
            await logs_channel.send(embed=embed)
            return


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingMessageDelete(bot))

