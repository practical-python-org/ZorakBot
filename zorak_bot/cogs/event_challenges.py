import discord
from discord.ext import commands
from discord import default_permissions
import datetime
from discord.ext import tasks
from __main__ import bot
from ._settings import normal_channel

class _challenges(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command()
	async def challenge(self, ctx, day: discord.Option(str)):
		isAdmin = ctx.author
		if 'Staff' in [role.name for role in isAdmin.roles]:
			with open('50-Days-of-Python.txt', encoding='utf-8') as file:
				file = file.read()
				file = file.replace('Day ','$$$$$Day ')
				all_days = file.split('$$$$$')
				for current_day in all_days:
					if current_day.startswith(f'Day {day}:'):

						# Make the embed
						embed=discord.Embed(title=f"Practical Python's 50 days of code"
							, description=f"Please place only **finished answers** in the thread. Any challenge related discussions should happen in the help channels."
							, color=discord.Color.dark_green())
						embed.set_thumbnail(url='https://raw.githubusercontent.com/Xarlos89/PracticalPython/main/logo.png')
						embed.add_field(name=f'Challenge #{day}:'
							, value=current_day
							, inline=True)
						embed.set_footer(text=f"Brought to you by: Benjamin Bennett Alexander's 50 Days of Python ")
						await ctx.respond(embed=embed)

						# Open the thread
						channel = await bot.fetch_channel(normal_channel['challenges_channel']) # CHALLENGES channel
						thread = await ctx.channel.create_thread(name=f'Challenge #{day}'
								, type=discord.ChannelType.public_thread)

						help1 = await bot.fetch_channel(normal_channel['python_help_1'])
						help2 = await bot.fetch_channel(normal_channel['python_help_2'])
						await thread.send(f"Please place only **finished answers** for **Day {day}** in this thread.\nAny challenge related discussions should happen in {help1.mention} or {help2.mention}.")
		else:
			await ctx.respond('Only a member of the <@&960232134356901959> can launch a challenge.'
				, ephemeral=True)
			
def setup(bot):
	bot.add_cog(_challenges(bot))