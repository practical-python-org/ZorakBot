"""
Asks an eightball a question.
"""
from random import choice
import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralEightBall(commands.Cog):
    """
    Asks an eightball a question.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(aliases=["8ball"])
    async def eightball(self, ctx, question):
        """
        Asks a question to a magic 8-ball
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
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
                "Sure",
                "In what world will that ever happen",
                "As i see it no.",
                "No doubt about it",
                "Focus",
                "Unfortunately yes",
                "Unfortunately no,",
                "Signs point to no",
            ]
        )
        await ctx.respond(f"Question: {question}\n🎱 - {answer}")


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralEightBall(bot))
