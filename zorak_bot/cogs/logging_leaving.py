import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from asyncio import sleep
from __main__ import bot

class logging_leaving(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if 'Needs Approval' in [role.name for role in member.roles]:
			return
		else:
			logs_channel = await bot.fetch_channel(953543179133665380) # Welcome channel
			embed = discord.Embed(title='', description=f'<@{member.id}> has left us.', color=discord.Color.red())
			await logs_channel.send(embed=embed)


def setup(bot):
	bot.add_cog(logging_leaving(bot))