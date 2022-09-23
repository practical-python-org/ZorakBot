
import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge", "clr", "clean"])
    @commands.has_role("Staff")
    @commands.cooldown(1, 500, commands.BucketType.user)
    async def clear(self, ctx, amount, range=None):
        audit = self.bot.get_channel(953545221260595280)
        await ctx.message.delete() #Is this like a test?
        try:
            if amount >= 200: #bit of an odd function, need to ask what it's use case is exactly
                source_server = self.bot.get_guild(ctx.guild.id)
                source_channel = source_server.get_channel(ctx.channel.id)
                start_message = await source_channel.fetch_message(amount)
                if range != None:
                    end_message = await source_channel.fetch_message(range)
                    await ctx.channel.purge(after=start_message, before=end_message)
                else:
                    await ctx.channel.purge(after=start_message)
                await audit.send(f"{ctx.author.mention} deleted some messages in {ctx.channel}")
            if amount <= 50:
                await ctx.channel.purge(limit=amount), await audit.send(f"{ctx.author} deleted {amount} messages in {ctx.channel}")

        except:
            embed = discord.Embed(title="ERROR", description="")
            embed.add_field(name="Reason:", value="Plese either check the range or that the number is under 50!")
            await ctx.channel.send(embed=embed)
            
    @commands.command() #Is this for admins to set rules?
    async def rules(self, ctx, *, args): #Could save and load json and work with dicts, generally nicer to work with.
        if ctx.message.author.guild_permissions.administrator: #Could use the has role wrapper
            text = args.replace("!rules", "").split("\n")
            
            embed = discord.Embed(title=text[0], description="", timestamp=ctx.message.created_at) #there's a Embed.from_dict() function that can be pretty nice for generalising an embed format.
            for index, content in enumerate(text, 1):   
                if int(index) >= 2:
                    embed.add_field(name='Rule #'+str(index-1) , value=content)
            await ctx.message.delete()
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Permission denied: with little power comes... no responsibility?", reference=ctx.message)


def setup(bot):
    bot.add_cog(AdminCog(bot))