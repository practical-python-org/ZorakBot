import discord
from discord.ext import commands
from discord import default_permissions
from __main__ import bot

class admin_utility(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command()
	@commands.has_permissions(manage_messages=True)
	async def embed(self, ctx, title, content):
		# text = ctx.message.content.split("\n")
		embed = discord.Embed(title=title)
		# text.pop(0)
		# TODO: Fix this boi here  (didn't fix much but changed slightly)
		# [embed.add_field(name=f" ----- ", value=item, inline=False) for item in text]  # Nice
		embed.add_field(name='Content', value=content)
		# embed.set_footer(icon_url=ctx.author.avatar_url)
		# await ctx.message.delete()
		await ctx.send(embed=embed)

	"""
	Error handling for the entire Admin Cog
	"""
	async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"Sorry, {ctx.author.name}, you dont have permission to use this command!", reference=ctx.message)
		else:
			raise error


def setup(bot):
	bot.add_cog(admin_utility(bot))