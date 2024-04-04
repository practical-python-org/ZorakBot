"""
Logging for role changes. Logs the user who did the changing, the target user and the role.
"""
from discord.ext import commands

from zorak.utilities.cog_helpers.guild_settings import GuildSettings
from zorak.utilities.cog_helpers._embeds import (  # pylint: disable=E0401
    embed_role_add,
    embed_role_remove,
)


class LoggingRoles(commands.Cog):
    """
    Simple listener to on_member_update
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Checks what roles were changed, and logs it in the log channel.
        Can be quite spammy.
        """
        settings = GuildSettings(self.bot.settings.server, before.guild)
        current_guild = self.bot.get_guild(before.guild)
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == "AuditLogAction.member_role_update":
            target_member = audit_log.target
            responsible_member = audit_log.user

            changed_roles = []
            logs_channel = await self.bot.fetch_channel(settings.mod_log)
            if len(before.roles) > len(after.roles):
                for role in before.roles:
                    if role not in after.roles:
                        changed_roles.append(role)
                for item in changed_roles:
                    embed = embed_role_remove(target_member, responsible_member, item)
                    await logs_channel.send(embed=embed)

            elif len(before.roles) < len(after.roles):
                for role in after.roles:
                    if role not in before.roles:
                        changed_roles.append(role)
                for item in changed_roles:
                    embed = embed_role_add(target_member, responsible_member, item)
                    await logs_channel.send(embed=embed)



def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingRoles(bot))
