"""
Logs member bans
"""
from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import embed_ban  # pylint: disable=E0401


class LoggingBans(commands.Cog):
    """
    Simple listener to on_member_remove
    then checks the audit log for exact details
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        First we don't log bans for unapproved people.
        then we grab the guild, and from there read the last entry in the audit log.
        """
        if "Needs Approval" in [role.name for role in member.roles]:
            return

        settings = self.bot.db_client.get_guild_settings(member.guild)

        current_guild = self.bot.get_guild(settings["id"])
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == "AuditLogAction.ban":
            if audit_log.target == member:
                embed = embed_ban(member, audit_log)

                logs_channel = await self.bot.fetch_channel(settings["mod_log"])
                await logs_channel.send(embed=embed)
                return


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingBans(bot))
