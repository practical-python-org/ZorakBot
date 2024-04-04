"""
logs when someone makes a ticket.
"""
from discord.ext import commands

from zorak.utilities.cog_helpers.guild_settings import GuildSettings
from zorak.utilities.cog_helpers._embeds import (  # pylint: disable=E0401
    embed_ticket_create,
    embed_ticket_delete,
    embed_ticket_remove,
    embed_ticket_update,
)


class Loggingthreads(commands.Cog):
    """
    Logs all form of thread creation and deletion when [ticket] is involved.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        """
        When a thread is created
        """
        settings = GuildSettings(self.bot.settings.server, thread.guild)

        current_guild = thread.guild

        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)]
        entry = audit_log[0]

        target = "AuditLogAction.thread_create"
        if str(entry.action) == target and str(entry.target).startswith("[Ticket]"):
            mod_log = await self.bot.fetch_channel(settings.mod_log)
            embed = embed_ticket_create(entry.user, entry.target.mention)
            await mod_log.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_thread_update(self, before):
        """
        When a thread is updated, deleted or removed.
        """
        settings = GuildSettings(self.bot.settings.server, before.guild)
        current_guild = before.guild

        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)]
        entry = audit_log[0]
        update = "AuditLogAction.thread_update"
        delete = "AuditLogAction.thread_delete"
        remove = "AuditLogAction.thread_remove"

        if str(entry.action) == update and str(entry.target).startswith("[Ticket]"):
            logs_channel = await self.bot.fetch_channel(settings.mod_log)
            embed = embed_ticket_update(entry.user, before.id)
            await logs_channel.send(embed=embed)
            return

        if str(entry.action) == delete and str(entry.target).startswith("[Ticket]"):
            logs_channel = await self.bot.fetch_channel(settings.mod_log)
            embed = embed_ticket_delete(entry.user, before.id)
            await logs_channel.send(embed=embed)
            return

        if str(entry.action) == remove and str(entry.target).startswith("[Ticket]"):
            logs_channel = await self.bot.fetch_channel(settings.mod_log)
            embed = embed_ticket_remove(entry.user, before.id)
            await logs_channel.send(embed=embed)
            return


def setup(bot):
    """
    Required.
    """
    bot.add_cog(Loggingthreads(bot))
