import discord
import requests
from discord.ext import commands

class CodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def runcode(self, ctx):  # Could dump message context into the string and return it
        await ctx.send("""To run python code in the chat, type: \./run python \`\`\`py Your code here \`\`\`""", reference=ctx.message)

    @commands.command()
    async def codeblock(self, ctx):
        await ctx.send(
            """To format your python code like this: ```py x = 'Hello World!' ``` Type this: \`\`\`py Your code here \`\`\`""",
            reference=ctx.message,
        )

    @commands.command(aliases=["pip", "pypi"])
    async def pipsearch(self, ctx):
        package = ctx.message.content.split(" ")[-1]

        if not package:
            await ctx.send(
                embed=discord.Embed(
                    title='Traceback (most recent call): "~/ur_brain"', description="Invalid pacakge name!", colour=discord.Colour.red()
                )
            )
        else:
            data = requests.get(f"https://pypi.org/pypi/{package}/json").json()
            embed = discord.Embed(
                title=f"Searched {package}",
                description=f"[Project URL]({data['info']['package_url']})",
                colour=discord.Colour.green(),
                timestamp=ctx.message.created_at,
            )

            embed.add_field(name=f"{data['info']['name']}-{data['info']['version']}", value=f"{data['info']['summary']}")
            embed.set_footer(text=f"Requested by {ctx.message.author}")
            await ctx.send(embed=embed)

    @commands.command(aliases=["git"])
    async def github(self, ctx, *, endpoint):
        try:
            info = requests.get(f"https://api.github.com/repos/{endpoint}").json()
            contrib_info = requests.get(f"https://api.github.com/repos/{endpoint}/contributors").json()
            embed = discord.Embed(
                title=info["name"],
                description=f"[Repository Link]({info['html_url']})",
                colour=discord.Colour.green(),
                timestamp=ctx.message.created_at,
            )

            embed.add_field(name="Owner", value=info["owner"]["login"])
            embed.add_field(name="Language", value=info["language"])
            embed.add_field(name="Stars", value=info["stargazers_count"])
            embed.add_field(name="Forks", value=info["forks"])
            embed.add_field(name="License", value=info["license"]["name"] if info["license"] is not None else "None")
            embed.add_field(name="Open Issues", value=info["open_issues"])
            embed.add_field(name="Contributors", value="\n".join([contribs["login"] for contribs in contrib_info]))
            embed.set_thumbnail(url=info["owner"]["avatar_url"])
            embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            return embed
        except:
            embed = discord.Embed(
                title="Oops", description="Repository does not existz.", colour=discord.Colour.red(), timestamp=ctx.message.created_at
            )
            embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed, reference=ctx.message)

    @github.error  # odd but cool, be good as a generalized error wrapper if possible
    async def no_endpoint(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(
                    title="No endpoint",
                    description="Please add an endpoint!\n`Syntax: !github|!git <username/repo_name>`",
                    timestamp=ctx.message.created_at,
                    colour=discord.Colour.red(),
                ),
                reference=ctx.message,
            )


def setup(bot):
    bot.add_cog(CodeCog(bot))
