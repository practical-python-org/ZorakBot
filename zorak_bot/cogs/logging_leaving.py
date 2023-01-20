import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from asyncio import sleep
from __main__ import bot
from ._settings import log_channel, server_info


class logging_leaving(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		current_guild = bot.get_guild(server_info['id'])

		# Dont log kicks for unapproved people. 
		if 'Needs Approval' in [role.name for role in member.roles]:
			return

		audit_log = [entry async for entry in current_guild.audit_logs(limit=1)]
		entry = audit_log[0]

		if str(entry.action) == 'AuditLogAction.kick':
			if entry.target == member:

				logs_channel = await bot.fetch_channel(log_channel['mod_log'])
				embed=discord.Embed(title=f'{member} was kicked'
									, description=f'By: {entry.user}'
									, color=discord.Color.red()
									, timestamp=datetime.utcnow())
				embed.add_field(name= f'Reason:'
							, value=f'{entry.reason}'
							, inline=True) 
				await logs_channel.send(embed=embed)
				return

		elif str(entry.action) == 'AuditLogAction.ban':
			if entry.target == member:

				logs_channel = await bot.fetch_channel(log_channel['mod_log'])
				embed=discord.Embed(title=f'{member} was banned'
									, description=f'By: {entry.user}'
									, color=discord.Color.red()
									, timestamp=datetime.utcnow())
				embed.add_field(name= f'Reason:'
							, value=f'{entry.reason}'
							, inline=True) 
				await logs_channel.send(embed=embed)
				return
				
		else:
			logs_channel = await bot.fetch_channel(log_channel['join_log']) # Welcome channel
			await logs_channel.send(f'<@{member.id}> has left us.')





def setup(bot):
	bot.add_cog(logging_leaving(bot))