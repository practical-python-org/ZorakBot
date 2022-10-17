from random import choice
from discord.ext import commands

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rolldice(self, ctx):
        await ctx.send(f"**{ctx.message.author.name}** rolled a **{choice(range(1,7))}**", reference=ctx.message)

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx):
        answer = choice(
            [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs points to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not to tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good",
                "Very doubtful.",
                "Be more polite.",
                "How would i know",
                "100%",
                "Think harder",
                "Sure" "In what world will that ever happen",
                "As i see it no.",
                "No doubt about it",
                "Focus",
                "Unfortunately yes",
                "Unfortunately no,",
                "Signs point to no",
            ]
        )
        await ctx.send("🎱 - " + answer, reference=ctx.message)


def setup(bot):
    bot.add_cog(GamesCog(bot))
