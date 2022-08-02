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
<<<<<<< HEAD
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

=======
                f"         -**Cannot** **preview**-\n-"
                f"**Make sure message is in this server,"
                f" and not a text file or image**-")

@bot.command()
async def suggest(ctx, *, args):
	await ctx.message.delete()
	embed = discord.Embed(description=args, timestamp=ctx.message.created_at)
	embed.set_author(name=f"Suggestion by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
	msg = await ctx.send(embed=embed)
	await msg.add_reaction("👍")	
	await msg.add_reaction("👎")

@bot.command()
async def poll(ctx):
	await ctx.message.delete()
	reactions = {
		'1': '1️⃣',
		'2': '2️⃣',
		'3': '3️⃣',
		'4': '4️⃣',
		'5': '5️⃣',
		'6': '6️⃣',
		'7': '7️⃣',
		"8": '8️⃣',
		"9": '9️⃣',
		"10": '🔟'
	}
	text = ctx.message.content.replace("!poll", "").split("\n")

	if len(text) < 4:
		await ctx.send("Can't create a poll! Please provide more options.")
	elif len(text) > 12:
		await ctx.send("Can't create a poll! Please provide only 10 options.")
	else:
		embed = discord.Embed(
			description=f"**{text[1]}**\n\n"+"\n\n".join(f"{reactions[str(idx)]}: {opt}" for idx, opt in enumerate(text[2:], 1)),
			timestamp=ctx.message.created_at
		)
		embed.set_author(name=f"Poll by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

		msg = await ctx.send(embed=embed)
		
		for idx in range(1, len(text[2:]) + 1):
			await msg.add_reaction(reactions[str(idx)]), await ctx.message.delete()

@bot.command(aliases=["av"])
async def avatar(
        ctx,
        member: discord.Member = None):
    embed = Utility_Funcs.get_avatar(ctx, member)
    await ctx.send(embed=embed, reference=ctx.message)


@bot.command(aliases=["whois"])
async def userinfo(ctx, member: Member = None):
	if not member:
		member = ctx.message.author

	roles = [role for role in member.roles]

	embed = discord.Embed(
		colour=discord.Colour.orange(),
		timestamp=ctx.message.created_at,
		title=str(member.display_name)
	)
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f"Requested by {ctx.message.author}")

	embed.add_field(name="Username:", value=member.name, inline=False)
	embed.add_field(name="ID:", value=member.id, inline=False)

	embed.add_field(name="Account Created On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
	embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

	try:
		embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
		embed.add_field(name="Highest Role:", value=member.top_role.mention)
		
		await ctx.send(embed=embed)

	except:
		await ctx.send(embed=discord.Embed(title="Traceback (most recent call last): \"~/ur_brain\"", colour=discord.Colour.red(), description="NoRoleError: Please get atleast one role for yourself"))

@bot.command(aliases=["pip", "pypi"])
async def pipsearch(ctx):
	package = ctx.message.content.split(" ")[-1]
	
	if not package:
		await ctx.send(embed=discord.Embed(title="Traceback (most recent call): \"~/ur_brain\"", description="Invalid pacakge name!", colour=discord.Colour.red()))
	else:
		data = Utility_Funcs.getPypiInfo(package)
		
		embed=discord.Embed(
			title=f"Searched {package}",
			description=f"[Project URL]({data['info']['package_url']})",
			colour=discord.Colour.green(),
			timestamp=ctx.message.created_at,
		)

		embed.add_field(name=f"{data['info']['name']}-{data['info']['version']}", value=f"{data['info']['summary']}")
		embed.set_footer(text=f"Requested by {ctx.message.author}")
		await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
	await ctx.send(embed=Utility_Funcs.zong(ctx, bot))

@bot.command(aliases=["git"])
async def github(ctx, *, endpoint):
    await ctx.send(embed=Utility_Funcs.getgitinfo(ctx, endpoint),
                   reference=ctx.message)
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
>>>>>>> parent of 2ee684f (Moved error into Error handling area.)


@bot.command(aliases=["tex"])
async def latex(ctx, *, expr):
	res = Utility_Funcs.render_latex(expr, ctx)

	await ctx.message.delete()
	await ctx.send(embed=res[0], file=res[1])

@bot.command()
async def help(ctx):
	embed = discord.Embed(title="User-Commands", description=Utility_Funcs.help_msg(), timestamp=ctx.message.created_at)
	await ctx.send(embed=embed, reference=ctx.message)


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


if __name__ == "__main__":
	bot.run(TOKEN)
	

	EXTENSION_FOLDER = 'groups'
	for file in os.listdir(EXTENSION_FOLDER):
		if file.endswith('.py') and file != "__init__.py":
			module_path = f"{EXTENSION_FOLDER}.{os.path.splitext(file)[0]}"
			bot.load_extension(module_path)

