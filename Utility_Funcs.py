#### Any utility should stay here. 
import requests
from datetime import datetime
import pytz
import discord
from io import BytesIO
from matplotlib import mathtext, font_manager
import matplotlib as mpl

mpl.rcParams['savefig.transparent'] = True
mpl.rcParams['text.color'] = "white"

texFont = font_manager.FontProperties(size=30, family='serif', math_fontfamily='cm')

requests.packages.urllib3.disable_warnings()

def zong(ctx, bot): # Alias for the Z.ping command
	return(discord.Embed(
		title="Pong.",
		description=f"Zorak's current ping is **{round(bot.latency * 1000)}ms**",
		timestamp=ctx.message.created_at,
		color=discord.Color.green()))

def runcode():
	return """
To run python code in the chat, type:

\./run python
\`\`\`py
Your code here
\`\`\`
"""

def codeblock():
	return """
	To format your python code like this:
```py
x = 'Hello World!'
```
Type this:

\`\`\`py
Your code here
\`\`\`
"""


def get_times():
    # India
    tz_india = datetime.now(tz=pytz.timezone("Asia/Kolkata"))
    # Japan
    tz_japan = datetime.now(tz=pytz.timezone("Asia/Tokyo"))
    # America
    tz_america_ny = datetime.now(tz=pytz.timezone("America/New_York"))
    # Austria- Vienna
    tz_austria = datetime.now(tz=pytz.timezone("Europe/Vienna"))
    Times = (f"Japan (Chiaki): {tz_japan.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nIndia (777advait): {tz_india.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nAustria (Xarlos): {tz_austria.strftime('%m/%d/%Y %I:%M %p')}"
             f"\nAmerica (Minus): {tz_america_ny.strftime('%m/%d/%Y %I:%M %p')} ")
    return Times

    
def make_embed(message, author, created_at, avatar):
	text = message.split("\n")
	embed = discord.Embed(title=text[0], timestamp=created_at)
	text.pop(0)
	[embed.add_field(name=f" ----- ", value=text[index], inline=False) for index,item in enumerate(text)]
	embed.set_footer(icon_url=avatar, text=author)
	return embed

def get_avatar(ctx, member):
    if not member:
        member = ctx.author
    embed = discord.Embed(
        title=f"Avatar for {member}",
        description=f"[Download image]({member.avatar_url})",
        timestamp=ctx.message.created_at,
    )
    embed.set_image(url=member.avatar_url)
    return embed

def Run_zeus(url):
	if "https://" in url == True:
			try:
					requests.get(url=url, timeout=2.5, verify=False)
					context = (url, "**ONLINE**")
			except requests.exceptions.ConnectionError:
					context = (url, "**OFFLINE**")

	else:
			fix_url = f"https://{url}"
			try:
					requests.get(url=fix_url, timeout=2.5, verify=False)
					context = (fix_url, "**ONLINE**")
			except requests.exceptions.ConnectionError:
					context = ("INVALID URL", "Please try again")

	return context	

# z.preview
# z.suggest
# z.poll
# z.avatar
# z.owo

def help_msg():
	return """
***For-fun commands***
- z.hello
- z.catfact
- z.dogfact
- z.pugfact
- z.quote
- z.joke
- z.8ball [question]
- z.taunt
- z.rolldice
- z.owo [text]
- z.catpic
- z.dogpic [breed] (Optional)
- z.pokedex [pokemon]
	
***Utility Commands***
- z.codeblock
- z.runcode
- z.preview
- z.google [question]
- z.embed </br>[title]</br>[content]  
- z.zeus [website]
- z.fakeperson
- z.poll </br>[title]</br>[options]
- z.suggest [suggestion]
- z.avatar/z.av [member] (default=author)
- z.userinfo/z.whois [member] (Optional)
- z.pipsearch/z.pypi/z.pip [package]
- z.ping
- z.git/z.github [endpoint]
	"""


def getPypiInfo(package):
	return requests.get(f"https://pypi.org/pypi/{package}/json").json()


def getgitinfo(ctx, endpoint):
	try:
		info = requests.get(f"https://api.github.com/repos/{endpoint}").json()
		contrib_info = requests.get(f"https://api.github.com/repos/{endpoint}/contributors").json()
		embed = discord.Embed(
			title=info["name"],
			description=f"[Repository Link]({info['html_url']})",
			colour=discord.Colour.green(),
			timestamp=ctx.message.created_at)
	
		embed.add_field(name="Owner",value=info["owner"]["login"])
		embed.add_field(name="Language",value=info["language"])
		embed.add_field(name="Stars",value=info["stargazers_count"])
		embed.add_field(name="Forks",value=info["forks"])
		embed.add_field(name="License",value=info["license"]["name"] if info["license"] is not None else "None")
		embed.add_field(name="Open Issues",value=info["open_issues"])
		embed.add_field(name="Contributors",value="\n".join([contribs["login"] for contribs in contrib_info]))
		embed.set_thumbnail(url=info["owner"]["avatar_url"])
		embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
		return embed
	except:
		embed = discord.Embed(
			title="Oops",
			description="Repository does not existz.",
			colour=discord.Colour.red(),
			timestamp=ctx.message.created_at)
		embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
	return embed


def render_latex(tex_expr, ctx):
	buff = BytesIO()
	
	mathtext.math_to_image(
		rf"${tex_expr}$".replace("\n", " "),
		buff,
		dpi = 300,
		prop=texFont,
		format="png"
	)

	buff.seek(0)

	file = discord.File(
		fp=buff,
		filename="expr.png"
	)

	embed = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at)
	embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	embed.set_image(url="attachment://expr.png")

	return (embed, file)