from discord.ext import commands
from datetime import datetime
from __main__ import bot, log_channels
import discord

class error_handler(commands.Cog, command_attrs=dict(hidden=True)):
	def __init__(self, bot):
		self.bot = bot


	@bot.event
	async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
		error_channel = bot.get_channel(log_channels['zorak_log'])

		embed = discord.Embed(title=f'<:red_circle:1043616578744357085> Zorak error!'
			, description=f'{ctx.author} used /{ctx.command} in <#{ctx.channel}>'
			, color=discord.Color.dark_red()
			, timestamp=datetime.utcnow())
		embed.add_field(name='Traceback (most recent call last): '
			, value=f'```py\n{error}```')

		await error_channel.send(ctx.author.mention)
		await error_channel.send(embed=embed)


def setup(bot):
	bot.add_cog(error_handler(bot))