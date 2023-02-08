import discord
from discord.ext import commands
from datetime import datetime
from __main__ import bot
from ._settings import log_channel


class logging_avatars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar != after.avatar:

            embed = discord.Embed(
                title=f"{before} updated their profile picture!",
                color=discord.Color.dark_grey(),
                timestamp=datetime.utcnow(),
            )
            embed.set_thumbnail(url=after.avatar)

            logs_channel = await bot.fetch_channel(log_channel["user_log"])
            await logs_channel.send(f"<@{before.id}>", embed=embed)


def setup(bot):
    bot.add_cog(logging_avatars(bot))
