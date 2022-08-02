from random import choice
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Member
import Error_Handling
import Admin_Funcs
import Fun_Funcs
import Utility_Funcs
import os, math
import discord

TOKEN = os.environ['TOKEN']
bot = Bot(command_prefix=["z.", "Z."])
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you..."))
	print('{0.user}, ready to conquer the world.'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(Error_Handling.get_error_msg(error),
                       reference=ctx.message)
    await ctx.message.delete()
#-----------------------------#  Administrator Commands


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		msg = "**You're still on cooldown!! next avaliable in {:.2f}s".format(error.retry_after)
		alert = bot.get_channel(953545221260595280)
		await alert.send(f"{ctx.author.mention}\n {msg}")



"""   

				Utility Commands

"""

@bot.listen('on_message')
async def preview(message):
	if message.content.startswith(
		"https://discord.com/channels/"
	) is True or message.content.startswith(
			"https://discordapp.com/channels/") is True:
		try:
			link = message.content.replace("/", " ").split(" ")
			sourceServer = bot.get_guild(int(link[4]))
			sourceChannel = sourceServer.get_channel(int(link[5]))
			sourceMessage = await sourceChannel.fetch_message(int(link[6]))

			embed = discord.Embed(title="**Message** **Preview**",description="",timestamp=sourceMessage.created_at)

			if len(sourceMessage.content) <= 1000:
				embed.add_field(name="**Content:** ",value=sourceMessage.content)
			elif len(sourceMessage.content) > 1000:
				# This just breaks the source message into 950 character chunks in a list.
				chunks = [sourceMessage.content[i:i + 950]for i in range(0, len(sourceMessage.content), 950)]
				for chunk in chunks: # for each item in the chunk list, add a field to the embed.
					embed.add_field(name="**---------**",value=f"```py\n{chunk}\n```",inline=False)

			embed.set_footer(text=sourceMessage.author,icon_url=sourceMessage.author.avatar_url)
			await message.channel.send(embed=embed)

		except:
			await message.channel.send(
				f"         -**Cannot** **preview**-\n-"
				f"**Make sure message is in this server,"
				f" and not a text file or image**-")


"""   

				Error Handling

"""

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("User you requested cannot be found.",
                       reference=ctx.message)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Zorak has no such command!", reference=ctx.message)
    await ctx.message.delete()

@github.error
async def no_endpoint(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send(
			embed=discord.Embed(
				title="No endpoint",
				description="Please add an endpoint!\n`Syntax: !github|!git <username/repo_name>`",
				timestamp=ctx.message.created_at,
				colour=discord.Colour.red()
			),
			reference=ctx.message
		)

if __name__ == "__main__":
	bot.run(TOKEN)
	

	EXTENSION_FOLDER = 'groups'
	for file in os.listdir(EXTENSION_FOLDER):
		if file.endswith('.py') and file != "__init__.py":
			module_path = f"{EXTENSION_FOLDER}.{os.path.splitext(file)[0]}"
			bot.load_extension(module_path)

