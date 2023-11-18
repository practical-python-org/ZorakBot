"""
A listener that looks for repeat messages and destroys them.
"""
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.utils import get

from zorak.utilities.cog_helpers._embeds import (
    embed_spammer,  # pylint: disable=E0401
)

class ModerationSpamMessages(commands.Cog):
    """
    Destroying spam with bots
    """

    def __init__(self, bot):
        self.bot = bot
        self.last_message = discord.Message
        self.uber_last_message = discord.Message


    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Scans every message and compares them
        """
        time_ago = datetime.utcnow() - timedelta(seconds=5)

        # Dont catch Zorak
        if message.author == self.bot.user:
            return

        # When message is not spam...
        if self.last_message != message.content:
            self.uber_last_message = self.last_message
            self.last_message = message
            return

        # When message IS spam...
        # last message is the same as the current message
        if self.last_message == message.content:
            # The channel however, is different.

            if self.last_message.channel != message.channel:
                await message.channel.send(
                    f"{message.author.mention}"
                    f"\nPlease do not post the same message in multiple channels.")
                # Load those roles, and get ready to activate.
                naughty = get(message.author.server.roles, name="Naughty")
                quarantine = await self.bot.fetch_channel(self.bot.server_settings.user_roles.bad["naughty"])

                # If user has sent 3 messages that are exactly the same, pull the trigger.
                if message.content == self.last_message.content == self.uber_last_message.content:

                    # timeout that boi
                    message.author.timeout(
                        until=datetime.timedelta(minutes=10)
                        , reason="Duplicate message was detected in multiple channels.")

                    # assign Naughty roll
                    await self.bot.add_roles(message.author, naughty)

                    # Post the message in Quarantine channel
                    await quarantine.send(embed=embed_spammer(message.content))

                    # delete the messages
                    await self.bot.uber_last_message.delete()
                    await self.bot.last_message.delete()
                    await message.delete()


def setup(bot):
    """
    Required.
    """
    bot.add_cog(ModerationSpamMessages(bot))
