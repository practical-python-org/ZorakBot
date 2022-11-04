import discord
from discord.ext import commands
from discord.utils import get

from __main__ import bot

class admin_verification(discord.ui.View):

	@discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.success)
	async def verify_button_callback(self, button, interaction):
		user = interaction.user
		guild = interaction.guild
		roles = guild.roles
		role = discord.utils.get(roles, id=935466692316917770)
		welcome = f"""
Awesome, {user.mention}. Thank you for verifying. 
Allow me to introduce you {guild.name}.

First, why dont you read over our {bot.get_channel(953583540044443689).mention}
Next, why not add some {bot.get_channel(965927411273302076).mention}?
After that, how about introducing yourself in {bot.get_channel(953543179133665380).mention}?

We have awesome {bot.get_channel(953583598429171742).mention} that cover courses, IDE's and text editors, as well as project ideas and documentation.

If you have any questions, feel free to post your question in {bot.get_channel(903542455675260928).mention} or {bot.get_channel(903542494409674803).mention}
I'm availible any time by typing /help

Looking forward to having you here!
"""

		if 'Needs Approval' in [role.name for role in user.roles]:
			await user.remove_roles(role)
			await user.send(welcome)
		else:
			await user.send('You have already been Verified. Go away.')



class verify_helper(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.has_permissions(manage_messages=True)
	@commands.slash_command(description='Adds verify button to channel.')# Create a slash command
	async def add_verify_button(self, ctx):
		await ctx.respond("Please Verify that you are not a bot.", view=admin_verification(timeout=None))
	
	"""
	Error handling for the entire Admin Cog
	"""
	async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"Sorry, {ctx.author.name}, you dont have permission to use this command!", reference=ctx.message)
		else:
			raise error
def setup(bot):
	bot.add_cog(verify_helper(bot))