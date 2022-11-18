import discord
from discord.ext import commands
from discord import default_permissions
from __main__ import bot

class admin_logging(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@bot.event
	async def on_member_remove(member):
		if 'Needs Approval' in [role.name for role in member.roles]:
			return
		else:
			logs_channel = await bot.fetch_channel(953543179133665380) # Welcome channel
			embed = discord.Embed(title='', description=f'{member.name} has left us.', color=discord.Color.red())
			await logs_channel.send(embed=embed)





def setup(bot):
	bot.add_cog(admin_logging(bot))
