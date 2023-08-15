"""
Uses get request to check if the video is a rick roll using keywords on youtube.
"""
import logging
import requests
from discord.ext import commands


logger = logging.getLogger(__name__)


class RickRollScanner(commands.Cog):
    """
    Uses youtube get request to check if the video is a rick roll using keywords.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Check for potential rick roll by video id")
    async def imbored(self, ctx, prompt):
        """
        Send a get request to youtube to check if the video is a rick roll
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        gen_url = f"https://www.youtube.com/watch?v={prompt}"
        data = requests.get(
            gen_url, timeout=5).text
        
        forbidden_keywords = [
            "rickroll",
            "roll",
            "rickroll'd",
            "rick",
            "astley",
            "never",
            "gonna",
            "give",
            "you",
            "up",
        ]

        if any(keyword in data.lower() for keyword in forbidden_keywords):
            await ctx.respond(
                f"Warning! {ctx.author.name} that might be a rick roll."
            )
        else:
            await ctx.respond(
                f"{ctx.author.name} might not be a rick roll."
            )

def setup(bot):
    """
    Required.
    """
    bot.add_cog(RickRollScanner(bot))
