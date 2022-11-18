import discord
from discord.ext import commands
from discord import default_permissions
from __main__ import bot

class admin_moderation(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot
	"""

		----- New member events -----

	"""
	@bot.event
	async def on_member_join(member):
		guild = member.guild

		welcome_message = f"""
Hi there, {member.mention}
I'm Zorak, the moderatior of {guild.name}.

We are very happy that you have decided to join us.
Before you are allowed to chat, you need to verify that you aren't a bot.
Dont worry, it's easy. Just go to {bot.get_channel(953545059888930816).mention} and click the green button.

After you do, all of {guild.name} is availibe to you. Have a great time :-)
"""

		# Add verification role
		await member.add_roles(member.guild.get_role(935466692316917770))

		#Send Welcome Message
		await member.send(welcome_message)
		

def setup(bot):
	bot.add_cog(admin_moderation(bot))
	