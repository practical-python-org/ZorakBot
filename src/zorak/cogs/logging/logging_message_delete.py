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
        settings = self.bot.db_client.get_guild_settings(message.guild)
        current_guild = settings["id"]
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]
        logs_channel = await self.bot.fetch_channel(settings["chat_log"])

        logger.info(f" --- A message by {message.author.name} was deleted...")

        # If the audit log is triggered, it means someone OTHER than the author deleted the message.
        # https://discordpy.readthedocs.io/en/stable/api.html
        # ?highlight=audit%20log#discord.AuditLogAction.message_delete
        if str(audit_log.action) == 'AuditLogAction.message_delete' and audit_log.user.id == message.author.id:
            logger.info(f" --- {audit_log.user.name}'s action triggered the audit log.")

            # TODO: refactor the embed to accept both the person that triggered the audit log, and the message author.
            embed = embed_message_delete(audit_log.user, message)
            await logs_channel.send(embed=embed)

        else:
            # Otherwise, the author deleted it.
            username = message.author

            # I think this is causing the issue with staff ghost-deleting messages.
            # for role in message.author.roles:
            #     if role.id in [settings['staff_role'], settings["admin_role"], settings["owner_role"]]:
            #         await logs_channel.send(embed=embed_message_delete(username, message))
            #         return
            logger.info(f" --- {username.name}'s action DID NOT trigger the audit log.")
            await logs_channel.send(f"{username.mention}", embed=embed_message_delete(username, message))


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingMessageDelete(bot))
