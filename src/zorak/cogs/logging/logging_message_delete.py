"""
logs when a message is deleted.
"""
from datetime import datetime
import logging
import discord
from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import embed_message_delete

logger = logging.getLogger(__name__)


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
        If a mod deletes, take the audit log event. If a user deletes, handle it normally.
        """
        # Don't record edits in Staff only channels.
        if message.channel.category_id == 940543787250364486:  # This is the ID of the "staff area" category.
            # Yes, that's hardcoded. Suck it.
            return

        current_guild = message.guild
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]
        logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["chat_log"])

        # If the audit log is triggered, it means someone OTHER than the author deleted the message.
        # https://discordpy.readthedocs.io/en/stable/api.html?highlight=audit%20log#discord.AuditLogAction.message_delete

        # print(audit_log)
        # print(f"-> {audit_log.action}")
        # print(f"-> {audit_log.after}")
        # print(f"-> {audit_log.before}")
        # print(f"-> {audit_log.category}")
        # print(f"-> {audit_log.changes}")
        # print(f"-> {audit_log.created_at}")
        # print(f"-> {audit_log.extra}")
        # print(f"-> {audit_log.guild}")
        # print(f"-> {audit_log.id}")
        # print(f"-> {audit_log.reason}")
        # print(f"-> {audit_log.target}")
        # print(f"-> {audit_log.user}")

        if str(audit_log.action) == 'AuditLogAction.message_delete':
            # Then a moderator deleted a message.
            embed = embed_message_delete(audit_log.target, message, audit_log.user)
            await logs_channel.send(embed=embed)

        else:
            # Otherwise, the author deleted it.
            username = message.author
            await logs_channel.send(f"{username.mention}", embed=embed_message_delete(username, message))


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingMessageDelete(bot))
