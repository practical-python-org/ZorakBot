"""
Simple coinflip command. 
"""
import logging
import random
from random import choice
import time
from discord.ext import commands

logger = logging.getLogger(__name__)

class GambaSlots(commands.Cog):
    """
    # GAMBA?!
    """

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🐍", "👑", "🌈", "🐌", "💸"]
        if message.content.startswith('!slots'):
            new_message = await message.channel.send("Spinning ...")
            for _ in range(3):
                selected_emojis = random.choices(emojis, k=3)
                await new_message.edit(content="Spinning: " +" ".join(selected_emojis))
                time.sleep(0.5)
            final_emojis = random.choices(emojis, k=3)
            await new_message.edit(content="Final: " + " ".join(final_emojis))

def setup(bot):
    """
    Required.
    """
    bot.add_cog(GambaSlots(bot))