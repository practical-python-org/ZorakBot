"""
A simple sarcastic google command.
"""
import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralSarcasticGoogle(commands.Cog):
    """
    # Creates a link to the Let me google that for you site.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def google(self, ctx, question):
        """
        sarcastically googles a question.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond(
            f"Here, allow me to google that one for you:"
            f"\nhttps://letmegooglethat.com/?q={question.replace(' ', '+')}"
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralSarcasticGoogle(bot))
