import logging
import os
from flask import Flask
from threading import Thread

import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot
import zorak_bot.core.admin as admin
import zorak_bot.core.play as play
import zorak_bot.util.general as general
from zorak_bot.util.args_util import parse_args
from zorak_bot.util.logging_util import setup_logger

logger = logging.getLogger(__name__)

app = Flask(__name__)

bot = Bot(command_prefix=["z.", "Z."])
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you..."))
	print('{0.user}, ready to conquer the world.'.format(bot))

@app.route('/')
def index():
    return 'Zorak, Ready to conquer the world.'

#-----------------------------#  Administrator Commands
@bot.command()
async def echo(ctx, *, message=None):
    """
    Echos a message. If no message, it will alert the user.
    Args:
        ctx: discord context : dictionary
        message: message to display : str
    Returns:
        None
    """
    await ctx.message.delete()
    await ctx.send(admin.send_echo(message))

@bot.command()
@commands.has_role("Staff")
async def dailychallenge(ctx, day):
        await ctx.send(admin.get_challange(day=day))

@bot.command()
@commands.has_role("Staff")
async def addChallange(ctx, day, *, text):
	await admin.add_challange(day=day, text=text)
	await ctx.send("ADDED!!!"), await ctx.message.delete()

@bot.command()
@commands.has_role("Staff")
async def toc(ctx):
	await ctx.send(admin.contents), await ctx.message.delete()

@bot.command()
async def rules(ctx, *, args):
	if ctx.message.author.guild_permissions.administrator:
		text = args.replace("!rules", "").split("\n")
		
		embed = discord.Embed(title=text[0], description="", timestamp=ctx.message.created_at)
		for index, content in enumerate(text, 1):
			if int(index) >= 2:
				embed.add_field(name='Rule #'+str(index-1) , value=content)
		await ctx.message.delete()
		await ctx.send(embed=embed)
	else:
		await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)

@bot.command(aliases=["purge", "clr", "clean"])
@commands.has_role("Staff")
@commands.cooldown(1, 500, commands.BucketType.user)
async def clear(ctx, amount: int, range2=None):
    audit = bot.get_channel(953545221260595280)
    await ctx.message.delete()
    try:
        if amount >= 200:
            sourceServer = bot.get_guild(ctx.guild.id)
            sourceChannel = sourceServer.get_channel(ctx.channel.id)
            startMessage = await sourceChannel.fetch_message(amount)
            if range2 != None:
                endMessage = await sourceChannel.fetch_message(range2)
                await ctx.channel.purge(after=startMessage, before=endMessage)
            else:
                await ctx.channel.purge(after=startMessage)
            await audit.send(f"{ctx.author.mention} deleted some messages in {ctx.channel}")
        if amount <= 50:
            await ctx.channel.purge(limit=amount), await audit.send(f"{ctx.author} deleted {amount} messages in {ctx.channel}")

    except:
        embed = discord.Embed(title="ERROR", description="")
        embed.add_field(name="Reason:", value="Plese either check the range or that the number is under 50!")
        await ctx.channel.send(embed=embed)




@bot.command()
async def times(ctx):
	embed = discord.Embed(title=f"**TIMES**", description="")
	embed.add_field(name="Staff", value=general.get_times())
	await ctx.send(embed=embed)

#-----------------------------#  User "Fun" Commands
@bot.command()
async def hello(ctx):
	await ctx.send(play.hello(), reference=ctx.message)

@bot.command()
async def taunt(ctx):
	await ctx.send(play.taunt(), reference=ctx.message)
	
@bot.command()
async def catfact(ctx):
	await ctx.send(play.catfact(), reference=ctx.message)

@bot.command()
async def dogfact(ctx):
	await ctx.send(play.dogfact(), reference=ctx.message)

@bot.command()
async def pugfact(ctx):
	await ctx.send(play.pugFact(), reference=ctx.message)

@bot.command()
async def catpic(ctx):
	await ctx.send(file=discord.File(fp=play.catpic(), filename="cat.png"), reference=ctx.message)

@bot.command()
async def joke(ctx):
	await ctx.send(play.joke(), reference=ctx.message)
	
@bot.command()
async def quote(ctx):
	await ctx.send(play.quote(), reference=ctx.message)

@bot.command(aliases=["8ball"])
async def eightball(ctx):
	await ctx.send('🎱 - ' + play.eightball(), reference=ctx.message)
	
@bot.command()
async def fakeperson(ctx):
	await ctx.send(play.fakePerson(), reference=ctx.message)

@bot.command()
async def rolldice(ctx):
	await ctx.send(f"**{ctx.message.author.name}** rolled a **{play.dice()}**", reference=ctx.message)

@bot.command()
async def google(ctx, *, args):
	await ctx.send(f"Here, allow me to google that one for you:\nhttps://letmegooglethat.com/?q={args.replace(' ', '+')}",reference=ctx.message)

@bot.command()
async def pokedex(ctx, *, pokemon):
    await ctx.send(embed=play.pokedex(pokemon))
    
@bot.command()
async def dogpic(ctx, *, breed=None):
    await ctx.send(embed=play.dogpic(breed))

"""   

				Utility Commands

"""
@bot.command()
async def runcode(ctx):
	await ctx.send(general.runcode(), reference=ctx.message)
	
@bot.command()
async def codeblock(ctx):
	await ctx.send(general.codeblock(), reference=ctx.message)

@bot.command()
async def embed(ctx, *, args):
    embed = general.make_embed(ctx.message.content, 
								 ctx.message.author,
                                 ctx.message.created_at,
                                 ctx.message.author.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command()
async def zeus(ctx, *, args):
	res = general.Run_zeus(url=args)

	if res[1] == "**ONLINE**":
		COLOR = discord.Color.green()
	else:
		COLOR = discord.Color.red()

	embed = discord.Embed(title="ZeusTheInvestigator", description="", timestamp=ctx.message.created_at, color=COLOR)
	embed.add_field(name=f"Checked link: *{res[0]}*", value=f"STATUS: {res[1]}")
	embed.set_footer(text="Credits to: @777advait#6334")

	await ctx.send(embed=embed)

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
    embed = general.get_avatar(ctx, member)
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
		data = general.getPypiInfo(package)
		
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
	await ctx.send(embed=general.zong(ctx, bot))

@bot.command(aliases=["git"])
async def github(ctx, *, endpoint):
    await ctx.send(embed=general.getgitinfo(ctx, endpoint),
                   reference=ctx.message)

@bot.command(aliases=["tex"])
async def latex(ctx, *, expr):
	res = general.render_latex(expr, ctx)

	await ctx.message.delete()
	await ctx.send(embed=res[0], file=res[1])

@bot.command()
async def help(ctx):
	embed = discord.Embed(
		title="User-Commands",
		 description=general.help_msg(),
		  timestamp=ctx.message.created_at)
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

def main_thread():
	main()
def webserver_thread():
	app.run(debug=False, port=80, host='0.0.0.0')

def main() -> None:
	args = parse_args()
	setup_logger(
        level=args.log_level,
        stream_logs=args.console_log,
		log_file=args.log_file,
		err_file=args.err_file
    )
	logger.info(f"Arguments Passed {args}")
	logger.info("Logger initialised")
	logger.info("Attempting to run Zorak")
	if args.discord_token is not None:
		bot.run(args.discord_token)
	else:
		bot.run(os.environ['TOKEN'])

if __name__ == "__main__":
    main_thread.start()
    webserver_thread.start()