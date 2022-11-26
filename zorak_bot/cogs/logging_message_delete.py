import discord
from discord import Member
from discord.ext import commands
from datetime import datetime
from __main__ import bot

class logging_message_delete(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

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
			, value=message.content # ToDo: This throws an error when deleting an embed. 
			, inline=True)

		logs_channel = await bot.fetch_channel(954023390375710751) # ADMIN message log
		await logs_channel.send(embed=embed)


def setup(bot):
	bot.add_cog(logging_message_delete(bot))