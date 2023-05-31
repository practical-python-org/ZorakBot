from discord.ext import commands
from ._settings import log_channel, server_info
from utilities.cog_helpers._embeds import embed_ticket_create, embed_ticket_update, embed_ticket_delete, embed_ticket_remove


class logging_threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        current_guild = self.bot.get_guild(server_info["id"])

        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)]
        entry = audit_log[0]

        if str(entry.action) == "AuditLogAction.thread_create" and str(entry.target).startswith('[Ticket]'):
            mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
            embed = embed_ticket_create(entry.user, entry.target.mention)
            await mod_log.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        current_guild = self.bot.get_guild(server_info["id"])

        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)]
        entry = audit_log[0]
        if str(entry.action) == "AuditLogAction.thread_update" and str(entry.target).startswith('[Ticket]'):
            logs_channel = await self.bot.fetch_channel(log_channel["mod_log"])
            embed = embed_ticket_update(entry.user, before.id)
            await logs_channel.send(embed=embed)
            return

        elif str(entry.action) == "AuditLogAction.thread_delete" and str(entry.target).startswith('[Ticket]'):
            logs_channel = await self.bot.fetch_channel(log_channel["mod_log"])
            embed = embed_ticket_delete(entry.user, before.id)
            await logs_channel.send(embed=embed)
            return

        elif str(entry.action) == "AuditLogAction.thread_remove" and str(entry.target).startswith('[Ticket]'):
            logs_channel = await self.bot.fetch_channel(log_channel["mod_log"])
            embed = embed_ticket_remove(entry.user, before.id)
            await logs_channel.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(logging_threads(bot))
