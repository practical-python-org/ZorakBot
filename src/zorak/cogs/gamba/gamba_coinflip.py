"""
Simple coinflip command. 
"""
import logging
import random
from random import choice
from discord.ext import commands

logger = logging.getLogger(__name__)

class GambaCoinflip(commands.Cog):
    """
    # GAMBA?!
    """

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        
        # !coinflip heads 1000
        
        if message.content.startswith('!coinflip'):
            
            parsed = message.content.split()
            heads_or_tails = parsed[1]
            
            try: 
                points = int(parsed[2])
            except ValueError:
                await message.channel.send("You need to bet full points!")
                return
            if heads_or_tails not in ["heads", "tails"]:
                await message.channel.send("You can only bet on heads or tails!")
                return

            if points < 0:
                await message.channel.send("You betting negative points? You are a madman!")
                return

            if points == 0:
                await message.channel.send("You betting zero points? You are a coward!")
                return

            if points > 0:

                if points > self.bot.db_client.get_user_points(message.author.id):
                    await message.channel.send("You don't have enough points!")
                    return

                await message.channel.send("Flipping the coin...")
                coin = random.choice(["heads", "tails"])

                if coin == heads_or_tails:
                    await message.channel.send(f"The coin landed on {coin}! You won {points} points!")
                    self.bot.db_client.add_points_to_user(message.author.id, points)
                    return
                else:
                    await message.channel.send(f"The coin landed on {coin}! You lost {points} points!")
                    self.bot.db_client.add_points_to_user(message.author.id, -points)
                    return

            await message.channel.send("Something went wrong.")
            return

def setup(bot):
    """
    Required.
    """
    bot.add_cog(GambaCoinflip(bot))