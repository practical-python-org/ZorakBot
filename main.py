from discord.ext.commands import Bot
from z_keep_alive import keep_alive
from discord.ext import owoify
from discord import Member
import Admin_Funcs
import Fun_Funcs
import Utility_Funcs
import os, math
import discord
import datetime

bot = Bot("!")
bot.remove_command("help")

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you..."))
	print('{0.user}, ready to conquer the world.'.format(bot))

#-----------------------------#  Administrator Commands
@bot.command()
async def echo(ctx, *, args):
	if ctx.message.author.guild_permissions.administrator:
		await ctx.message.delete()
		try:
			await ctx.send(args)
		except:
			await ctx.send("Please enter a message to echo.", reference=ctx.message)

	else:
		await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)

@bot.command()
async def dailychallenge(ctx):
	if ctx.message.author.guild_permissions.administrator:
		await ctx.send(Admin_Funcs.DailyChallenge())
		Admin_Funcs.increaseDay()
	else:
		await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)

@bot.command()
async def rules(ctx, *, args):
	if ctx.message.author.guild_permissions.administrator:
		text = args.replace("!rules", "").split("\n")
		
		embed = discord.Embed(title=text[0], description="", timestamp=datetime.datetime.utcnow())
		for index, content in enumerate(text, 1):
			if int(index) >= 2:
				embed.add_field(name='Rule #'+str(index-1) , value=content)
		await ctx.message.delete()
		await ctx.send(embed=embed)
	else:
		await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)

#-----------------------------#  User "Fun" Commands
@bot.command()
async def hello(ctx):
	await ctx.send(Fun_Funcs.hello(), reference=ctx.message)

@bot.command()
async def taunt(ctx):
	await ctx.send(Fun_Funcs.taunt(), reference=ctx.message)
	
@bot.command()
async def catfact(ctx):
	await ctx.send(Fun_Funcs.catfact(), reference=ctx.message)

@bot.command()
async def dogfact(ctx):
	await ctx.send(Fun_Funcs.dogfact(), reference=ctx.message)

@bot.command()
async def pugfact(ctx):
	await ctx.send(Fun_Funcs.pugFact(), reference=ctx.message)

# @bot.command() # THIS DOES NOT WORK YET
# async def catpic(ctx):
# 	await ctx.send(Fun_Funcs.catpic(), reference=ctx.message)


@bot.command()
async def joke(ctx):
	await ctx.send(Fun_Funcs.joke(), reference=ctx.message)
	
@bot.command()
async def quote(ctx):
	await ctx.send(Fun_Funcs.quote(), reference=ctx.message)

@bot.command(aliases=["8ball"])
async def eightball(ctx):
	await ctx.send('🎱 - ' + Fun_Funcs.eightball(), reference=ctx.message)
	
@bot.command()
async def fakeperson(ctx):
	await ctx.send(Fun_Funcs.fakePerson(), reference=ctx.message)

@bot.command()
async def rolldice(ctx):
	await ctx.send(f"**{ctx.message.author.name}** rolled a **{Fun_Funcs.dice()}**", reference=ctx.message)

@bot.command()
async def google(ctx, *, args):
	await ctx.send(f"Here, allow me to google that one for you:\nhttps://letmegooglethat.com/?q={args.replace(' ', '+')}",reference=ctx.message)


	
#-----------------------------#  User "Utility" Commands
@bot.command()
async def runcode(ctx):
	await ctx.send(Utility_Funcs.runcode(), reference=ctx.message)
	
@bot.command()
async def codeblock(ctx):
	await ctx.send(Utility_Funcs.codeblock(), reference=ctx.message)

@bot.command()
async def embed(ctx):
	text = ctx.message.content.replace("!embed", "").split("\n")

	embed = discord.Embed(title=text[1], description="", timestamp=datetime.datetime.utcnow())

	if len(text) <= 3:
		embed.add_field(name="Content", value=text[2])
		await ctx.message.delete()
		await ctx.send(embed=embed)
	
	elif len(text) > 3:
		for i in range(2, len(text)):
			if len(text[i]) < 1:
				continue
			else:
				embed.add_field(name=f" ----- ", value=text[i], inline=False)

		embed.set_footer(icon_url=ctx.message.author.avatar_url, text=ctx.message.author.name)
		await ctx.message.delete()
		await ctx.send(embed=embed)

@bot.command()
async def zeus(ctx, *, args):
	res = Utility_Funcs.Run_zeus(url=args)

	if res[1] == "**ONLINE**":
		COLOR = discord.Color.green()
	else:
		COLOR = discord.Color.red()

	embed = discord.Embed(title="ZeusTheInvestigator", description="", timestamp=datetime.datetime.utcnow(), color=COLOR)
	embed.add_field(name=f"Checked link: *{res[0]}*", value=f"STATUS: {res[1]}")
	embed.set_footer(text="Credits to: @777advait#6334")

	await ctx.send(embed=embed)

@bot.command()
async def preview(ctx, *, args):
	if "https://discord.com/channels" in args:
		text = args
		l = text.replace(", ", " ").split(" ")
		key = "https://discord.com/channels/"
		for item in l:
				if key in item:
						try:
								lilink = l[l.index(item)]
								response = "-**---** Link Preview **---**- \n\n"
								link = lilink.replace("https://discord.com/channels/", "").split("/")
								sourceMessage = await bot.get_guild(int(link[-3])).get_channel(int(link[-2])).fetch_message(int(link[-1]))
	
								if len(sourceMessage.content) <= 1000:
										embed = discord.Embed(title=response, description="", timestamp=datetime.datetime.utcnow())
										embed.add_field(name=f"Length: {len(sourceMessage.content)}", value=sourceMessage.content)
										embed.set_footer(text=sourceMessage.author, icon_url=sourceMessage.author.avatar_url)
										await ctx.send(embed=embed)
	
								if len(sourceMessage.content) > 1000:
										contents = sourceMessage.content
										con2 = []
										splitstr = math.ceil(len(contents) / 1000)
										embed1 = discord.Embed(title=response, description="", timestamp=datetime.datetime.utcnow())
										while contents:
												con2.append(contents[:900])
												contents = contents[900:]
										for feilds in range(0, splitstr):
												embed1.add_field(name="----------------------", value=f"```py\n{con2[feilds]}\n```",
																				 inline=False)
										embed1.set_footer(text=sourceMessage.author, icon_url=sourceMessage.author.avatar_url)
										await ctx.send(embed=embed1)
						except:
								await ctx.send(f"-**Cannot** **preview**-\n-"
															f"**Make sure message is in this server,"
															f" and not a text file or image**-")

@bot.command()
async def suggest(ctx, *, args):
	await ctx.message.delete()
	embed = discord.Embed(description=args, timestamp=datetime.datetime.utcnow())
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
			timestamp=datetime.datetime.utcnow()
		)
		embed.set_author(name=f"Poll by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

		msg = await ctx.send(embed=embed)
		
		for idx in range(1, len(text[2:]) + 1):
			await msg.add_reaction(reactions[str(idx)])

@bot.command(aliases=["av"])
async def avatar(ctx, member: Member = None):
	if not member:
		member = ctx.author
	embed = discord.Embed(title=f"Avatar for {member}", description=f"[Download image]({member.avatar_url})", timestamp=datetime.datetime.utcnow())
	embed.set_image(url=member.avatar_url)
	await ctx.send(embed=embed, reference=ctx.message)

@bot.command()
async def owo(ctx, *, args):
	embed = discord.Embed(description=await owoify.owoify(args), timestamp=datetime.datetime.utcnow())
	embed.set_author(name=f"{ctx.message.author.display_name} OWO'd something!", icon_url=ctx.message.author.avatar_url)
	await ctx.send(embed=embed, reference=ctx.message)

@bot.command()
async def help(ctx):
	embed = discord.Embed(title="User-Commands", description=Utility_Funcs.help_msg(), timestamp=datetime.datetime.utcnow())
	await ctx.send(embed=embed, reference=ctx.message)

if __name__ == "__main__":
	keep_alive()
	try:
		bot.run(os.environ["TOKEN"])
	except:
	    os.system("kill 1")