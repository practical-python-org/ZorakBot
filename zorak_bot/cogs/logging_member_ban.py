import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from __main__ import bot
from ._settings import log_channel

class logging_bans(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_ban(self, guild, member: discord.Member):

			embed=discord.Embed(title=f'<:octagonal_sign:1046087417704226937> User Banned'
				, color=discord.Color.red()
				, timestamp=datetime.utcnow())

			embed.add_field(name= f'{member.name} was banned.'
				, value='If you feel this was a mistake, contact the Staff.'
				, inline=True) 

			logs_channel = await bot.fetch_channel(log_channel['mod_log']) # Welcome channel
			await logs_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(logging_bans(bot))