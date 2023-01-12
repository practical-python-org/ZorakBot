import re
import discord
from discord import Member
from datetime import datetime
from discord.ext import commands
from __main__ import bot
from ._settings import log_channel


class moderation_invites(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):

		txt = message.content
		current_channel = message.channel
		logs_channel = await bot.fetch_channel(log_channel['mod_log'])


		def is_invite(arg_message):
			#invitation types
			#Official covers official invites "discord.gg/s7s8df9a"
			#unofficial covers urls that start with d and end with letter numbers "dxxxx.gg/23bn2u2"
			official = re.search("(?:https?://)?(?:www\.|ptb\.|canary\.)?(?:discord(?:app)?\.(?:(?:com|gg)/invite/[a-z0-9-_]+)|discord\.gg/[a-z0-9-_]+)", arg_message) 
			unofficial = re.search("(?:https?://)?(?:www\.)?(?:dsc\.gg|invite\.gg+|discord\.link)/[a-z0-9-_]+", arg_message)
			if official is not None or unofficial is not None:
				return True
			else:
				return False

		def log_message(arg_message):
			author = arg_message.author
			embed = discord.Embed(title=f'<:red_circle:1043616578744357085> Invite removed'
				, description=f'Posted by {arg_message.author}\nIn {arg_message.channel.mention}'
				, color=discord.Color.dark_red()
				, timestamp=datetime.utcnow())
			embed.set_thumbnail(url=author.avatar)
			embed.add_field(name='Message: '
				, value=message.content # ToDo: This throws an error when deleting an embed. 
				, inline=True)
			return embed		


		def embed_warning(arg_message):
			author = arg_message.author
			embed = discord.Embed(title=f'<:x:1055080113336762408> External Invites are not allowed here!'
				, description=f'{arg_message.author}, your message was removed because it contained an external invite.\nIf this was a mistake, contact the @staff'
				, color=discord.Color.dark_red()
				, timestamp=datetime.utcnow())
			return embed	


		if is_invite(txt) is True:
			await logs_channel.send(embed=log_message(message))
			await message.delete()
			await current_channel.send(embed=embed_warning(message))

def setup(bot):
	bot.add_cog(moderation_invites(bot))