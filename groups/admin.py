import discord
from discord.ext import commands
import Admin_Funcs

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
    @commands.command()
    async def echo(self, ctx, *, message=None):
        """
        Echos a message. If no message, it will alert the user.
        Args:
            ctx: discord context : dictionary
            message: message to display : str
        Returns:
            None
        """
        await ctx.message.delete()
        await ctx.send(Admin_Funcs.send_echo(message))

    # @bot.command()
    # async def dailychallenge(ctx):
    # 	if ctx.message.author.guild_permissions.administrator:
    # 		await ctx.send(Admin_Funcs.DailyChallenge())
    # 		Admin_Funcs.increaseDay()
    # 	else:
    # 		await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)

    @commands.command()
    async def rules(self, ctx, *, args):
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

    @commands.command(aliases=["purge", "clr", "clean"])
    @commands.has_role("Staff")
    @commands.cooldown(1, 500, commands.BucketType.user)
    async def clear(self, ctx, amount: str):
        audit = self.client.get_channel(953545221260595280)
        if int(amount) <= 50:
            #set to 50 max to prevent wrongdoings.
            await ctx.channel.purge(limit=int(amount)), await audit.send(f"{ctx.author} deleted {amount} messages in {ctx.channel}")
        else:
            embed = discord.Embed(title="ERROR", description="")
            embed.add_field(name="Reason:", value="Invalid input- please choose a number 1-50")
            await ctx.channel.send(embed=embed)

def setup(client: commands.Bot):
    client.add_cog(Admin(client))