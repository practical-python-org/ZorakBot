import os
from discord.ext import commands

class DailyChallengeCog(commands.Cog):
    def __init__(self, bot):  # Could set current dict representing todays challenge here
        self.bot = bot

    @commands.command()
    @commands.has_role("Staff")
    async def dailychallenge(self, ctx, day):
        with open(clean_path(f"./Resources/DailyChallenges/day_{day}.txt"), "r") as f:
            text = f.read()
        await ctx.send(text.get_challange(day=day))

    @commands.command()
    @commands.has_role("Staff")
    async def add_challange(self, ctx, day, *, text):
        try:
            with open(clean_path(f'./Resources/DailyChallenges/day_{f"10{day}"}.txt'), "w") as f:
                f.write(text)
            await ctx.send("Added a new daily challenge."), await ctx.message.delete()
        except:
            await ctx.send("Failed adding a new daily challenge."), await ctx.message.delete()

    @commands.command()
    @commands.has_role("Staff")
    async def toc(self, ctx):
        await ctx.send(os.listdir(clean_path("./Resources/DailyChallenges"))), await ctx.message.delete()


def setup(bot):
    bot.add_cog(DailyChallengeCog(bot))
