import discord
from discord.ext import commands
import Fun_Funcs

class Fun(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(Fun_Funcs.hello(), reference=ctx.message)

    @commands.command()
    async def taunt(self, ctx):
        await ctx.send(Fun_Funcs.taunt(), reference=ctx.message)
        
    @commands.command()
    async def catfact(self, ctx):
        await ctx.send(Fun_Funcs.catfact(), reference=ctx.message)

    @commands.command()
    async def dogfact(self, ctx):
        await ctx.send(Fun_Funcs.dogfact(), reference=ctx.message)

    @commands.command()
    async def pugfact(self, ctx):
        await ctx.send(Fun_Funcs.pugFact(), reference=ctx.message)

    @commands.command()
    async def catpic(self, ctx):
        await ctx.send(file=discord.File(fp=Fun_Funcs.catpic(), filename="cat.png"), reference=ctx.message)

    @commands.command()
    async def joke(self, ctx):
        await ctx.send(Fun_Funcs.joke(), reference=ctx.message)
        
    @commands.command()
    async def quote(self, ctx):
        await ctx.send(Fun_Funcs.quote(), reference=ctx.message)

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx):
        await ctx.send('🎱 - ' + Fun_Funcs.eightball(), reference=ctx.message)
        
    @commands.command()
    async def fakeperson(self, ctx):
        await ctx.send(Fun_Funcs.fakePerson(), reference=ctx.message)

    @commands.command()
    async def rolldice(self, ctx):
        await ctx.send(f"**{ctx.message.author.name}** rolled a **{Fun_Funcs.dice()}**", reference=ctx.message)

    @commands.command()
    async def google(self, ctx, *, args):
        await ctx.send(f"Here, allow me to google that one for you:\nhttps://letmegooglethat.com/?q={args.replace(' ', '+')}",reference=ctx.message)

    @commands.command()
    async def pokedex(self, ctx, *, pokemon):
        await ctx.send(embed=Fun_Funcs.pokedex(pokemon))
        
    @commands.command()
    async def dogpic(self, ctx, *, breed=None):
        await ctx.send(embed=Fun_Funcs.dogpic(breed))

def setup(client: commands.Bot):
    client.add_cog(Fun(client))