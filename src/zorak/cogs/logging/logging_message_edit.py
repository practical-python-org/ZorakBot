"""
Logs when messages are edited.
"""
import logging
from discord.ext import commands

from zorak.utilities.cog_helpers.guild_settings import guild_settings
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
        self.settings = self.bot.settings.server

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        self.settings = guild_settings(self.settings, message_before.guild)

        # IGNORE /run, since we will set up an on_message_edit handler there with opposite logic
        if message_before.content.startswith('/run') or message_after.content.startswith('/run'):
            return

        elif message_before.content != message_after.content:
            # This guy here makes sure we use the displayed name inside the guild.
            if message_before.author.nick is None:
                username = message_before.author
            else:
                username = message_before.author.nick

            author = message_before.author

            for role in message_before.author.roles:
                # TODO: .admin_roles no longer exists, find a workaround here.
                if role.id not in self.settings.admin_roles:
                    # Dont log admin actions.
                    # This just gets really messy when we are cleaning things up
                    # or doing dodgy business in secret places.

                    embed = embed_message_edit(username, author, message_before, message_after)
                    logs_channel = await self.bot.fetch_channel(self.settings.chat_log)
                    await logs_channel.send(embed=embed)
                    return


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingMessageEdit(bot))
