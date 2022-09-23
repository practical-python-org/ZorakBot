

import discord
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)

class DiffusionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["drawme"])
    async def stable_diffusion(self, ctx, input, seed = None):
        sanetized = input.replace(" ", "-")
        gen_url = f"https://api.computerender.com/generate/{sanetized}"
        if seed:
            gen_url = gen_url+f"?seed={seed}"
        logger.info(gen_url)
        embed =  {
                "title": "Your Image",
                "color": 10848322,
                "image": {
                "url": gen_url
                }
        }
        
        await ctx.send(embed=discord.Embed.from_dict(embed))


def setup(bot):
    bot.add_cog(DiffusionCog(bot))

