"""
Logs when a member leaves.
"""
from discord.ext import commands

from zorak.utilities.cog_helpers.guild_settings import GuildSettings
from zorak.utilities.cog_helpers._embeds import embed_leave  # pylint: disable=E0401


class LoggingLeaving(commands.Cog):
    """
    Simple listener to on_member_remove
    then checks the audit log for exact details
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        First we don't log leaves for unapproved people.
        then we grab the guild, and from there read the last entry in the audit log.
        """
        if "Needs Approval" in [role.name for role in member.roles]:
            return

        settings = GuildSettings(self.bot.settings.server, member.guild)
        current_guild = self.bot.get_guild(member.guild)
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]

        if str(audit_log.action) != "AuditLogAction.ban" and str(audit_log.action) != "AuditLogAction.kick":
            embed = embed_leave(member)

            logs_channel = await self.bot.fetch_channel(settings.join_logs)
            await logs_channel.send(embed=embed)


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingLeaving(bot))
