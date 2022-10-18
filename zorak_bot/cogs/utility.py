import discord
from discord.ext import commands
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

# TODO: Avatars. shit doesn;t work. 
    # @commands.slash_command(description='Grabs the avatar of a user.')
    # async def avatar(self, ctx, member: discord.Option(str)):
    #     if member is 'me':
    #         member = ctx.author
    #     embed = discord.Embed(
    #         title=f"Avatar for {member}",
    #         description=f"[Download image]({discord.User.display_avatar})")
    #     embed.set_image(url=discord.User.display_avatar)
    #     await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(util(bot))