import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from __main__ import bot, logging

class error_logging(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_error(self, event,  *args, **kwargs):

			embed=discord.Embed(title=f'An error occurred'
				, color=discord.Color.red()
				, timestamp=datetime.utcnow())

			embed.add_field(name=event
				, value=args
				, inline=True) 

			logs_channel = await bot.fetch_channel(logging['zorak_log']) # Zorak Error Log
			await logs_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(error_logging(bot))