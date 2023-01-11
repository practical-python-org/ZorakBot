import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from __main__ import bot, log_channels

class logging_messages(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):
		if message_before.content != message_after.content:
			if message_before.author.nick is None:
				username = message_before.author
			else:
				username = message_before.author.nick

			author = message_before.author



			embed=discord.Embed(title=f'<:orange_circle:1043616962112139264> Message Edit'
				, description=f'Edited by {username}\nIn {message_after.channel.mention}'
				, color=discord.Color.dark_orange()
				, timestamp=datetime.utcnow())
			embed.set_thumbnail(url=author.avatar)
			embed.add_field(name='Original message: '
				, value=message_before.content
				, inline=True)

			embed.add_field(name= "After editing: "
				, value=message_after.content
				, inline=True)

			logs_channel = await bot.fetch_channel(log_channels['chat_log']) # ADMIN message log
			await logs_channel.send(f'{username.mention}',embed=embed)

def setup(bot):
	bot.add_cog(logging_messages(bot))