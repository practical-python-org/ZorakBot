"command group for utilities"
import discord
from discord import Member
from discord.ext import commands
import Utility_Funcs

class CustomHelp(commands.MinimalHelpCommand):
    pass

class Utility(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.client.help_command = CustomHelp
        self.client.help_command.cog = self

    @commands.command()
    async def runcode(self, ctx):
        await ctx.send(Utility_Funcs.runcode(), reference=ctx.message)
        
    @commands.command()
    async def codeblock(self, ctx):
        await ctx.send(Utility_Funcs.codeblock(), reference=ctx.message)

    @commands.command()
    async def embed(self, ctx, *, args):
        embed = Utility_Funcs.make_embed(ctx.message.content, 
                                    ctx.message.author,
                                    ctx.message.created_at,
                                    ctx.message.author.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def zeus(self, ctx, *, args):
        res = Utility_Funcs.Run_zeus(url=args)

        if res[1] == "**ONLINE**":
            COLOR = discord.Color.green()
        else:
            COLOR = discord.Color.red()

        embed = discord.Embed(title="ZeusTheInvestigator", description="", timestamp=ctx.message.created_at, color=COLOR)
        embed.add_field(name=f"Checked link: *{res[0]}*", value=f"STATUS: {res[1]}")
        embed.set_footer(text="Credits to: @777advait#6334")

        await ctx.send(embed=embed)


    @commands.command()
    async def suggest(self, ctx, *, args):
        await ctx.message.delete()
        embed = discord.Embed(description=args, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Suggestion by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")	
        await msg.add_reaction("👎")

    @commands.command()
    async def poll(self, ctx):
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

    @commands.command(aliases=["av"])
    async def avatar(self,
            ctx,
            member: discord.Member = None):
        embed = Utility_Funcs.get_avatar(ctx, member)
        await ctx.send(embed=embed, reference=ctx.message)


    @commands.command(aliases=["whois"])
    async def userinfo(self, ctx, member: Member = None):
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

    @commands.command(aliases=["pip", "pypi"])
    async def pipsearch(self, ctx):
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

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(embed=Utility_Funcs.zong(ctx, commands))

    @commands.command(aliases=["git"])
    async def github(self, ctx, *, endpoint):
        await ctx.send(embed=Utility_Funcs.getgitinfo(ctx, endpoint),
                    reference=ctx.message)



    @commands.command(aliases=["tex"])
    async def latex(self, ctx, *, expr):
        res = Utility_Funcs.render_latex(expr, ctx)

        await ctx.message.delete()
        await ctx.send(embed=res[0], file=res[1])

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="User-Commands",
            description=Utility_Funcs.help_msg(),
            timestamp=ctx.message.created_at)
        await ctx.send(embed=embed, reference=ctx.message)
    
    @commands.command()
    async def times(self, ctx):
        embed = discord.Embed(title=f"**TIMES**", description="")
        embed.add_field(name="Staff", value=Utility_Funcs.get_times())
        await ctx.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(Utility(client))