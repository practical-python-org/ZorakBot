import discord
from discord.ext import commands
from discord.utils import get
from __main__ import bot
import math
from io import BytesIO
import matplotlib.pyplot as plt 
import datetime
import requests
import pytz


class util(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Search Py-pi for a package.')
    async def pip_search(self, ctx, package: discord.Option(str)):
        data = requests.get(f"https://pypi.org/pypi/{package}/json").json()
        try:
            embed = discord.Embed(
                title=f"Searched {package}",
                description=f"[Project URL]({data['info']['package_url']})",
                colour=discord.Colour.green())
            embed.add_field(name=f"{data['info']['name']} version {data['info']['version']}"
                , value=f"{data['info']['summary']}")
            await ctx.respond(embed=embed)

        except:                
            await ctx.respond(
                    embed=discord.Embed(
                        title='Oops...'
                        , description="Invalid package name - " + package
                        , colour=discord.Colour.red()))
    
    @commands.slash_command(description='Search Github for a repo.')
    async def github_search(self, ctx, username: discord.Option(str),repo: discord.Option(str) ):
        try:
            info = requests.get(f"https://api.github.com/repos/{username}/{repo}").json()
            contrib_info = requests.get(f"https://api.github.com/repos/{username}/{repo}/contributors").json()
            embed = discord.Embed(
                title=info["name"],
                description=f"[Repository Link]({info['html_url']})",
                colour=discord.Colour.green())

            embed.add_field(name="Owner", value=info["owner"]["login"])
            embed.add_field(name="Language", value=info["language"])
            embed.add_field(name="Stars", value=info["stargazers_count"])
            embed.add_field(name="Forks", value=info["forks"])
            embed.add_field(name="License", value=info["license"]["name"] if info["license"] is not None else "None")
            embed.add_field(name="Open Issues", value=info["open_issues"])
            embed.add_field(name="Contributors", value="\n".join([contribs["login"] for contribs in contrib_info]))
            embed.set_thumbnail(url=info["owner"]["avatar_url"])
            await ctx.respond(embed=embed)
        except:
            embed = discord.Embed(
                title="Oops", description=f"Repository {username}/{repo} does not exist."
                , colour=discord.Colour.red())
            await ctx.respond(embed=embed)

    @commands.slash_command(description='Current times of Staff.')
    async def devtimes(self, ctx):  # again, dict mapping could be good to help here, could also provide a command with timezone as input. Could do a whole times cog probably.
        tz_india = datetime.datetime.now(tz=pytz.timezone("Asia/Kolkata"))
        tz_japan = datetime.datetime.now(tz=pytz.timezone("Asia/Tokyo"))
        tz_america_ny = datetime.datetime.now(tz=pytz.timezone("America/New_York"))
        tz_austria = datetime.datetime.now(tz=pytz.timezone("Europe/Vienna"))
        tz_uk = datetime.datetime.now(tz=pytz.timezone("GMT"))

        embed = discord.Embed(title=f"**Staff Times**", description="")
        embed.add_field(name="Austria (Xarlos):", value=f"{tz_austria.strftime('%m/%d/%Y %I:%M %p')}", inline=False)
        embed.add_field(name="Japan (Chiaki): ", value=f"{tz_japan.strftime('%m/%d/%Y %I:%M %p')}", inline=False)
        embed.add_field(name="India (777advait):", value=f"{tz_india.strftime('%m/%d/%Y %I:%M %p')}", inline=False)
        embed.add_field(name="America (Minus):", value=f"{tz_america_ny.strftime('%m/%d/%Y %I:%M %p')}", inline=False)
        embed.add_field(name="UK (Maszi):", value=f"{tz_uk.strftime('%m/%d/%Y %I:%M %p')}", inline=False)
        await ctx.respond(embed=embed)

    @commands.slash_command(description='Checks a URL to see if its online.')
    async def zeus(self, ctx, url: discord.Option(str)):
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

        if context[1] == "**ONLINE**":
            color = discord.Color.green()
        else:
            color = discord.Color.red()
        embed = discord.Embed(title="ZeusTheInvestigator", description="", color=color)
        embed.add_field(name=f"Checked link: *{context[0]}*", value=f"STATUS: {context[1]}")
        embed.set_footer(text="Credits to: @777advait#6334")
        await ctx.respond(embed=embed)



    @commands.Cog.listener()
    async def on_message(self, message):
        text = message.content
        link = text.replace(", ", " ")
        if link.startswith("https://discord.com/channels/")== True:
            link = link.split('/')
            response = "-**---** **Let** **me** **preview** **that** **for** **you.** **---**- \n\n"
            sourceServer = bot.get_guild(int(link[4]))
            sourceChannel = sourceServer.get_channel(int(link[5]))
            sourceMessage = await sourceChannel.fetch_message(int(link[6]))

            if len(sourceMessage.content) <= 1000:
                embed = discord.Embed(title=response, description="")
                embed.add_field(name=f"Length: {len(sourceMessage.content)}", value=sourceMessage.content)
                embed.set_footer(text=sourceMessage.author)
                await message.channel.send(embed=embed)

            elif len(sourceMessage.content) > 1000:
                contents = sourceMessage.content
                con2 = []
                splitstr = math.ceil(len(contents)/1000)
                embed1 = discord.Embed(title=response, description="")
                while contents:
                    con2.append(contents[:900])
                    contents = contents[900:]
                for feilds in range(0, splitstr):
                    embed1.add_field(name="------", value=f"```py\n{con2[feilds]}\n```", inline=False)
                embed1.set_footer(text=sourceMessage.author)
                await message.channel.send(embed=embed1) 



# # TODO: Hitting an import error in LaTeX
# # AttributeError: module 'matplotlib.pyplot' has no attribute 'mathtext'
#     @commands.slash_command(description='Sends a latex image.')
#     async def latex(self, ctx, expr: discord.Option(str)):
#         plt.rcParams["savefig.transparent"] = True
#         plt.rcParams["text.color"] = "white"
#         buff = BytesIO()
#         plt.mathtext.math_to_image(
#             f"${expr}$".replace("\n", " "),
#             buff,
#             dpi=300,
#             prop=plt.font_manager.FontProperties(size=30, family="serif", math_fontfamily="cm"),
#             format="png",
#         )
#         buff.seek(0)
#         embed = discord.Embed(colour=discord.Colour.green())
#         embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
#         embed.set_image(url="attachment://expr.png")
#         await ctx.respond(embed=embed, file=discord.File(fp=buff, filename="expr.png"))

# # TODO: Avatars. shit doesn't work. 
# # Issue is with "discord.User.display_avatar"
    # @commands.slash_command(description='Grabs the avatar of a user.')
    # async def avatar(self, ctx, member: discord.Option(str)):
    #     if member is 'me':
    #         member = ctx.author
    #     embed = discord.Embed(
    #         title=f"Avatar for {member}",
    #         description=f"[Download image]({discord.User.display_avatar})")
    #     embed.set_image(url=discord.User.display_avatar)
    #     await ctx.respond(embed=embed)

# # TODO: poll sends error
# # discord.errors.ApplicationCommandInvokeError: 
# # Application Command raised an exception: 
# # ValueError: too many values to unpack (expected 2)
#     @commands.slash_command()
#     async def poll(self, ctx, title, option1, option2, option3='', option4='', option5=''):
#         options = [option1,option2, option3,option4,option5]
#         reactions = ['1️⃣','2️⃣','3️⃣','4️⃣ ','5️⃣ ']
#         embed = discord.Embed(description=f"{title}")
#         for opt, num in options,reactions:
#             if opt != '':
#                 embed.add_field(name=num, value=opt, inline=False)
#         msg = await ctx.respond(embed=embed)
#         for idx, option in enumerate(options):
#             if option != '':
#                 await msg.add_reaction(reactions[str(idx)])


# # TODO: Does not see other members, only the author.
# # Figure out how to call up other users. 
#     @commands.slash_command(description='Sends info about a user.')
#     async def whois(self, ctx, member: discord.User):
#         if member is None:
#             member = ctx.author

#         roles = [role for role in bot.member.roles]
#         embed = discord.Embed(colour=discord.Colour.orange(), title=str(member.display_name))
#         # embed.set_thumbnail(url=member.avatar_url)
#         embed.set_footer(text=f"Requested by {ctx.author}")
#         embed.add_field(name="Username:", value=member.name, inline=False)
#         embed.add_field(name="ID:", value=member.id, inline=False)
#         embed.add_field(name="Account Created On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
#         embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
#         try:
#             embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
#             embed.add_field(name="Highest Role:", value=member.top_role.mention)
#         except:
#             pass
#         await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(util(bot))