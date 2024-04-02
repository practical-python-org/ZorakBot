"""
Simple coinflip command. 
"""
import logging
import random
from discord.ext import commands

logger = logging.getLogger(__name__)


class GambaCoinflip(commands.Cog):
    """
    # GAMBA?!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def coinflip(self, ctx, heads_or_tails, points):
        """
        A simple coinflip.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        
        if heads_or_tails not in ["heads", "tails"]:
            await ctx.respond("You can only bet on heads or tails!")
            return
        
        if points < 0:
            await ctx.respond("You betting negative points? You are a madman!")
            return
            
        if points == 0:
            await ctx.respond("You betting zero points? You are a coward!")
            return
        
        if points > 0:
            
            self.bot.db_client.get_user_points(ctx.author.id)
            
            if points > self.bot.db_client.get_user_points(ctx.author.id):
                await ctx.respond("You don't have enough points!")
                return

            await ctx.respond("Flipping the coin...")
            coin = random.choice(["heads", "tails"])
            
            if coin == heads_or_tails:
                await ctx.respond(f"The coin landed on {coin}! You won {points} points!")
                self.bot.db_client.add_points_to_user(ctx.author.id, points)
                return
            else:
                await ctx.respond(f"The coin landed on {coin}! You lost {points} points!")
                self.bot.db_client.add_points_to_user(ctx.author.id, -points)
                return

def setup(bot):
    """
    Required.
    """
    print("GambaCoinflip loaded.")
    bot.add_cog(GambaCoinflip(bot))