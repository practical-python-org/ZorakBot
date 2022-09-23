import logging
from io import BytesIO

import discord
import matplotlib as mpl
import requests
from discord.ext import commands

logger = logging.getLogger(__name__)
mpl.rcParams["savefig.transparent"] = True
mpl.rcParams["text.color"] = "white"


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Pong.",
                description=f"Zorak's current ping is **{round(self.bot.latency * 1000)}ms**",
                timestamp=ctx.message.created_at,
                color=discord.Color.green(),
            )
        )

    @commands.command()
    async def help(self, ctx):
        help_msg = """
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
            - z.drawme "text" (Required string) [seed] (Optional int)
                
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
        embed = discord.Embed(title="User-Commands", description=help_msg, timestamp=ctx.message.created_at)
        await ctx.send(embed=embed, reference=ctx.message)

    @commands.command()
    async def suggest(self, ctx, *, string_input):
        await ctx.message.delete()
        embed = discord.Embed(description=string_input, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Suggestion by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member=None):
        if not member:
            member = ctx.author
        embed = discord.Embed(
            title=f"Avatar for {member}",
            description=f"[Download image]({member.avatar_url})",
            timestamp=ctx.message.created_at,
        )
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed, reference=ctx.message)

    @commands.command()
    async def poll(self, ctx):
        await ctx.message.delete()
        reactions = {"1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣", "10": "🔟"}
        text = ctx.message.content.replace("!poll", "").split("\n")
        if len(text) < 4:
            await ctx.send("Can't create a poll! Please provide more options.")
        elif len(text) > 12:
            await ctx.send("Can't create a poll! Please provide only 10 options.")
        else:
            embed = discord.Embed(
                description=f"**{text[1]}**\n\n" + "\n\n".join(f"{reactions[str(idx)]}: {opt}" for idx, opt in enumerate(text[2:], 1)),
                timestamp=ctx.message.created_at,
            )
            embed.set_author(name=f"Poll by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=embed)
            for idx in range(1, len(text[2:]) + 1):
                await msg.add_reaction(reactions[str(idx)]), await ctx.message.delete()

    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, member=None):
        if not member:
            member = ctx.message.author
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=discord.Colour.orange(), timestamp=ctx.message.created_at, title=str(member.display_name))
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
            await ctx.send(
                embed=discord.Embed(
                    title='Traceback (most recent call last): "~/ur_brain"',
                    colour=discord.Colour.red(),
                    description="NoRoleError: Please get atleast one role for yourself",
                )
            )

    @commands.command(aliases=["tex"])
    async def latex(self, ctx, *, expr):
        buff = BytesIO()
        mpl.mathtext.math_to_image(
            f"${expr}$".replace("\n", " "),
            buff,
            dpi=300,
            prop=mpl.font_manager.FontProperties(size=30, family="serif", math_fontfamily="cm"),
            format="png",
        )
        buff.seek(0)
        embed = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        embed.set_image(url="attachment://expr.png")
        await ctx.message.delete()
        await ctx.send(embed=embed, file=discord.File(fp=buff, filename="expr.png"))

    @commands.command()
    async def zeus(self, ctx, *, url):
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
        embed = discord.Embed(title="ZeusTheInvestigator", description="", timestamp=ctx.message.created_at, color=color)
        embed.add_field(name=f"Checked link: *{context[0]}*", value=f"STATUS: {context[1]}")
        embed.set_footer(text="Credits to: @777advait#6334")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GeneralCog(bot))
