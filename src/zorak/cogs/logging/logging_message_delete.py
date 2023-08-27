"""
logs when a message is deleted.
"""
from datetime import datetime

import discord
from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import embed_message_delete


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
        Discord is stupid right now, and message deletes in the audit log suck,
        so we cant use this now.
        https://discordpy.readthedocs.io/en/stable/api.html
        ?highlight=audit%20log#discord.AuditLogAction.message_delete
        """
        current_guild = self.bot.get_guild(self.bot.server_settings.server_info['id'])
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]
        logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["chat_log"])
        # If the audit log is triggered, it means someone OTHER than the author deleted the message.
        if str(audit_log.action) == 'AuditLogAction.message_delete':
            member = current_guild.get_member(audit_log.user.id)
            embed = embed_message_delete(audit_log.user, message)
            await logs_channel.send(embed=embed)

            return
        else:
            # Otherwise, the author deleted it.
            username = message.author

            for role in message.author.roles:
                if role.id in self.bot.server_settings.admin_roles.values():
                    await logs_channel.send(embed=embed_message_delete(username, message))
                    return

            await logs_channel.send(f"{username.mention}", embed=embed_message_delete(username, message))


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingMessageDelete(bot))
