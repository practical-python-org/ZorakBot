import logging

import discord
from discord.ext import commands
from datetime import datetime


logger = logging.getLogger(__name__)


class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_channel = self.bot.settings.channels["zorak_log"]

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        error_log = await self.bot.fetch_channel(self.error_channel)

        # # This is just an interesting way of handling errors PER ERROR.
        # # For now, let's just catch all and redirect to logs and channel
        # if isinstance(error, commands.CommandOnCooldown):
        #     await ctx.respond("This command is currently on cooldown!")
        # else:
        #     raise error  # Here we raise other errors to ensure they aren't ignored

        embed = discord.Embed(title=f':red_circle: Zorak error!'
                              , description=f'{ctx.author} used /{ctx.command} in <#{ctx.channel}>'
                              , color=discord.Color.dark_red()
                              , timestamp=datetime.utcnow())
        embed.add_field(name='Traceback (most recent call last): '
                        , value=f'{error}')

        await error_log.send(ctx.author.mention)
        await error_log.send(embed=embed)
        logger.critical(error)


def setup(bot):
    bot.add_cog(error_handler(bot))
