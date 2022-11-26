import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from asyncio import sleep
from __main__ import bot

class logging_verification(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

#-------------------------------#
#								#
#   channel_verification_log	#
#								#
#-------------------------------#

	@commands.Cog.listener()
	###### On new join, do this
	async def on_member_join(self, member: discord.Member):
		# Add verification role
		await member.add_roles(member.guild.get_role(935466692316917770))

		# Log unverified join
		logs_channel = await bot.fetch_channel(1044302239616991242) # ADMIN user log
		embed = discord.Embed(title=''
			, description=f'{member.mention} joined, but has not verified.'
			, color=discord.Color.yellow())
		await logs_channel.send(embed=embed)

		# Send Welcome
		guild = member.guild
		welcome_message = f"""
Hi there, {member.mention}
I'm Zorak, the moderatior of {guild.name}.

We are very happy that you have decided to join us.
Before you are allowed to chat, you need to verify that you aren't a bot.
Dont worry, it's easy. Just go to {bot.get_channel(953545059888930816).mention} and click the green button.

After you do, all of {guild.name} is availibe to you. Have a great time :-)
"""
		#Send Welcome Message
		await member.send(welcome_message)
		time_unverified_kick = 3600 # 1 hour
		await sleep(time_unverified_kick)

		# Start verification timer
		if 'Needs Approval' in [role.name for role in member.roles]:
			# Kick timer, in seconds.
			time_unverified_kick = 3600 # 1 hour
			await sleep(time_unverified_kick)

			if 'Needs Approval' in [role.name for role in member.roles]:
				# Log the kick
				embed = discord.Embed(title=''
					, description=f'{member.mention} did not verify, auto-removed. ({time_unverified_kick*60} hour/s)'
					, color=discord.Color.red())
				await logs_channel.send(embed=embed)

				await member.kick(reason="Did not verify.")

def setup(bot):
	bot.add_cog(logging_verification(bot))