"""
Logs when messages are edited.
"""
import logging
from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import (
    embed_message_edit,  # pylint: disable=E0401
)

logger = logging.getLogger(__name__)


class LoggingMessageEdit(commands.Cog):
    """
    Simple listener to on_message_edit
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        # Ignore any bot messages
        if message_before.author.bot or message_after.author.bot:
            return

        # IGNORE /run, since we will set up an on_message_edit handler there with opposite logic
        if message_before.content.startswith('/run') or message_after.content.startswith('/run'):
            return

        elif message_before.content != message_after.content:
            # This guy here makes sure we use the displayed name inside the guild.

            if message_after.author.nick is None:
                username = message_after.author
            else:
                username = message_after.author.nick

            author = message_after.author

            embed = embed_message_edit(username, author, message_before, message_after)
            logs_channel = await self.bot.fetch_channel(self.bot.server_settings.log_channel["chat_log"])
            await logs_channel.send(embed=embed)


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingMessageEdit(bot))
