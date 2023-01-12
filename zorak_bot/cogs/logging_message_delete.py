import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from __main__ import bot
from ._settings import log_channel


class logging_message_delete(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_delete(self, message):

		if message.author.nick is None:
			username = message.author
		else:
			username = message.author.nick
			
		author = message.author

		embed = discord.Embed(title=f'<:red_circle:1043616578744357085> Deleted Message'
			, description=f'Deleted by {username}\nIn {message.channel.mention}'
			, color=discord.Color.dark_red()
			, timestamp=datetime.utcnow())
		embed.set_thumbnail(url=author.avatar)

		embed.add_field(name='Message: '
			, value=message.content # ToDo: This throws an error when deleting an embed. 
			, inline=True)

		logs_channel = await bot.fetch_channel(log_channel['chat_log'])
		await logs_channel.send(f'{username.mention}', embed=embed)


def setup(bot):
	bot.add_cog(logging_message_delete(bot))