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
		title="Zong!",
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

# !preview
# !suggest
# !poll
# !avatar
# !owo

def help_msg():
	return """
***For-fun commands***
- !hello
- !catfact
- !dogfact
- !pugfact
- !quote
- !joke
- !8ball [question]
- !taunt
- !rolldice
- !owo [text]
- !catpic
- !dogpic [breed] (Optional)
- !pokedex [pokemon]
	
***Utility Commands***
- !codeblock
- !runcode
- !preview
- !google [question]
- !embed </br>[title]</br>[content]  
- !zeus [website]
- !fakeperson
- !poll </br>[title]</br>[options]
- !suggest [suggestion]
- !avatar/!av [member] (default=author)
- !userinfo/!whois [member] (Optional)
- !pipsearch/!pypi/!pip [package]
- !ping
- !git/!github [endpoint]
	"""


def getPypiInfo(package):
	return requests.get(f"https://pypi.org/pypi/{package}/json").json()


def getgitinfo(endpoint):
	return requests.get(f"https://api.github.com/repos/{endpoint}").json()


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