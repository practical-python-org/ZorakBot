import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from asyncio import sleep
from __main__ import bot

class logging(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

#-------------------------------#
#								#
#   channel_verification_log	#
#								#
#-------------------------------#
	@commands.Cog.listener()
	###### On new join, do this
	async def on_member_join(self, member):
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
			time_unverified_kick = 5 # 1 hour
			await sleep(time_unverified_kick)

			if 'Needs Approval' in [role.name for role in member.roles]:
				# Log the kick
				embed = discord.Embed(title=''
					, description=f'{member.mention} did not verify, auto-removed. ({time_unverified_kick*60} hour/s)'
					, color=discord.Color.red())
				await logs_channel.send(embed=embed)

				await member.kick(reason="Did not verify.")



#-------------------------------#
#								#
#    channel_user_log_public	#
#								#
#-------------------------------#


	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if 'Needs Approval' in [role.name for role in member.roles]:
			return
		else:
			# logs_channel = await bot.fetch_channel(953543179133665380) # Welcome channel
			logs_channel = await bot.fetch_channel(953543179133665380) # Welcome channel
			embed = discord.Embed(title='', description=f'{member.name} has left us.', color=discord.Color.red())
			await logs_channel.send(embed=embed)

#-------------------------------#
#								#
#    channel_user_log_admin	    #
#								#
#-------------------------------#

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

			logs_channel = await bot.fetch_channel(953552502937243679) # ADMIN user log
			await logs_channel.send(embed=embed)


#-------------------------------#
#								#
#      channel_message_log	    #
#								#
#-------------------------------#

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		author = message.author

		embed = discord.Embed(title=f'<:red_circle:1043616578744357085> Deleted Message'
			, description=f'Deleted by {message.author.mention}\nIn {message.channel.mention}'
			, color=discord.Color.dark_red()
			, timestamp=datetime.utcnow())
		embed.set_thumbnail(url=author.avatar)
		embed.add_field(name='Message: '
			, value=message.content
			, inline=True)

		logs_channel = await bot.fetch_channel(954023390375710751) # ADMIN message log
		await logs_channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):
		if message_before.content != message_after.content:
			author = message_before.author

			embed=discord.Embed(title=f'<:orange_circle:1043616962112139264> Message Edit'
				, description=f'Edited by {message_before.author.mention}\nIn {message_after.channel.mention}'
				, color=discord.Color.dark_orange()
				, timestamp=datetime.utcnow())
			embed.set_thumbnail(url=author.avatar)
			embed.add_field(name='Original message: '
				, value=message_before.content
				, inline=True)

			embed.add_field(name= "After editing: "
				, value=message_after.content
				, inline=True)

			logs_channel = await bot.fetch_channel(954023390375710751) # ADMIN message log
			await logs_channel.send(embed=embed)




def setup(bot):
	bot.add_cog(logging(bot))