import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from __main__ import bot

class logging_nameChanges(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.nick != after.nick and before.nick is not None:

			embed=discord.Embed(title=f'<:grey_exclamation:1044305627201142880> Name Change'
				, description=f'Changed by: {before}.'
				, color=discord.Color.dark_grey()
				, timestamp=datetime.utcnow())
			embed.set_thumbnail(url=after.avatar)
			embed.add_field(name='Before', value=before.nick, inline=True)
			embed.add_field(name='After', value=after.mention, inline=True)

			logs_channel = await bot.fetch_channel(953552502937243679) # ADMIN user log
			await logs_channel.send(embed=embed)

		# Verification success logging	
		elif 'Needs Approval' in [role.name for role in before.roles] and 'Needs Approval' not in [role.name for role in after.roles]:
			logs_channel = await bot.fetch_channel(953543179133665380) # user join logs
			embed = discord.Embed(title='', description=f'{after.mention}, human number {after.guild.member_count} has joined.', color=discord.Color.dark_green())
			await logs_channel.send(embed=embed)


def setup(bot):
	bot.add_cog(logging_nameChanges(bot))