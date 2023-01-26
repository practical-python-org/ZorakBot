import discord
from discord.ext import commands
from __main__ import bot
from ._settings import log_channel, server_info
from datetime import datetime


class logging_threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        current_guild = bot.get_guild(server_info['id'])

        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)]
        entry = audit_log[0]

        if str(entry.action) == 'AuditLogAction.thread_update':
            logs_channel = await bot.fetch_channel(log_channel['mod_log'])
            embed = discord.Embed(title=f'{str(entry.user)} closed a ticket.'
                                  , description=f'Ticket: <#{before.id}>'
                                  , color=discord.Color.green()
                                  , timestamp=datetime.utcnow())
            await logs_channel.send(embed=embed)
            return

        elif str(entry.action) == 'AuditLogAction.thread_delete':
            logs_channel = await bot.fetch_channel(log_channel['mod_log'])
            embed = discord.Embed(title=f'{str(entry.user)} deleted a ticket.'
                                  , description=f'Ticket: <#{before.id}>'
                                  , color=discord.Color.red()
                                  , timestamp=datetime.utcnow())
            await logs_channel.send(embed=embed)
            return

        elif str(entry.action) == 'AuditLogAction.thread_remove':
            logs_channel = await bot.fetch_channel(log_channel['mod_log'])
            embed = discord.Embed(title=f'{str(entry.user)} removed a ticket.'
                                  , description=f'Ticket: <#{before.id}>'
                                  , color=discord.Color.red()
                                  , timestamp=datetime.utcnow())
            await logs_channel.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(logging_threads(bot))
