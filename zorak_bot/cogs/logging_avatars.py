import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from asyncio import sleep
from __main__ import bot, logging

class logging_avatars(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_user_update(self, before, after):
		if before.avatar != after.avatar:

			embed=discord.Embed(title=f'<:grey_exclamation:1044305627201142880> {before.name}'
				, color=discord.Color.dark_grey()
				, timestamp=datetime.utcnow())
			embed.set_thumbnail(url=after.avatar)
			embed.add_field(name='Avatar Update: '
				, value=before.mention
				, inline=True)

			logs_channel = await bot.fetch_channel(logging['user_log'])
			await logs_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(logging_avatars(bot))