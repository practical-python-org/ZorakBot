import logging

from discord.ext import commands, tasks

logger = logging.getLogger(__name__)


class PersistCog(commands.Cog):
    def __init__(self, bot):
        self.bit = 0
        self.bot = bot
        self.persist.start()

    @commands.command()
    @commands.is_owner()
    async def stop_persist(self, ctx):
        self.persist.cancel()

    @tasks.loop(seconds=300.0)
    async def persist(self):
        logger.debug("I'm creating some background noise!")  # Potentially not needed
        if self.bit == 0:
            self.bit = 1
        else:
            self.bit = 0

    @persist.before_loop
    async def before_persist(self):
        logger.info("Zorak is getting ready to create some background noise!")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(PersistCog(bot))
