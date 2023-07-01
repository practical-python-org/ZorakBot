"""
Logs when a user is kicked
"""
from discord.ext import commands

from zorak.cogs import log_channel, server_info  # pylint: disable=E0401
from zorak.utilities.cog_helpers._embeds import embed_kick  # pylint: disable=E0401


class LoggingKicks(commands.Cog):
    """
    Simple listener to on_member_remove
    then checks the audit log for exact details
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        First we don't log kicks for unapproved people.
        then we grab the guild, and from there read the last entry in the audit log.
        """
        if "Needs Approval" in [role.name for role in member.roles]:
            return

        current_guild = self.bot.get_guild(server_info["id"])
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == "AuditLogAction.kick":
            if audit_log.target == member:
                embed = embed_kick(member, audit_log)

                logs_channel = await self.bot.fetch_channel(log_channel["mod_log"])
                await logs_channel.send(embed=embed)
                return


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """

    bot.add_cog(LoggingKicks(bot))
