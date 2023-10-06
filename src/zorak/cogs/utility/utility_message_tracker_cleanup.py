"""
Detects message links, and sends a preview of the message that is linked.
"""
import math
import discord
from discord.ext import commands, tasks
from datetime import timedelta

class MessageTrackerCleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_tracker = {"test": {"created_at": discord.utils.utcnow(), "embed_id": "test"}}
        self.cleanup_message_tracker.start()

    @tasks.loop(hours=24)
    async def cleanup_message_tracker(self):
        current_time = discord.utils.utcnow()
        keys_to_remove = []
        
        for user_message_id, contents in self.message_tracker.items():
            message_date = contents["created_at"]
            if current_time - message_date >= timedelta(hours=24):
                keys_to_remove.append(user_message_id)
        
        for key in keys_to_remove:
            self.message_tracker.pop(key)

    @cleanup_message_tracker.before_loop
    async def before_cleanup_message_tracker(self):
        await self.bot.wait_until_ready()


def setup(bot):
    cleaner = MessageTrackerCleanup(bot)
    bot.add_cog(cleaner)
