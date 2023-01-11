import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from __main__ import bot, log_channels

class logging_unbans(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_unban(self, guild, member: discord.Member):

			embed=discord.Embed(title=f'<:green_circle:1046088647759372388> User Un-Banned'
				, color=discord.Color.red()
				, timestamp=datetime.utcnow())

			embed.add_field(name= f'{member.name} was un-banned.'
				, value='Welcome back.'
				, inline=True) 

			logs_channel = await bot.fetch_channel(log_channels['mod_log']) # Welcome channel
			await logs_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(logging_unbans(bot))