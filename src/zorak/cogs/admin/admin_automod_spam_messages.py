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


def same_author(current, old):
    if current.author == old.author:
        return True
    return False


def same_3_content(first, second, third):
    if first.content == second.content == third.content:
        return True
    return False


def same_3_author(first, second, third):
    if first.author == second.author == third.author:
        return True
    return False


def same_3_channel(first, second, third):
    if first.channel == second.channel == third.channel:
        return True
    return False


def is_second_message(first, second):
    if first.content == second.content:
        return True
    return False


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

        # Dont catch Zorak
        if message.author == self.bot.user:
            return

        print(f">{message.content} - {self.last_message.content} - {self.uber_last_message.content}")

        # When message is spam...
        if same_3_author(message, self.last_message, self.uber_last_message):
            if same_3_content(message, self.last_message, self.uber_last_message):
                if not same_3_channel(message, self.last_message, self.uber_last_message):
                    # Load those roles and channels
                    naughty = get(message.author.guild.roles, name="Naughty")
                    quarantine = await self.bot.fetch_channel(
                        self.bot.server_settings.channels["moderation"]["quarantine_channel"])

                    # timeout that boi
                    await message.author.timeout(
                        until=(datetime.now() + timedelta(seconds=10))
                        , reason="Duplicate message was detected in multiple channels.")

                    # assign Naughty roll
                    await message.author.add_role(naughty)

                    # Post the message in Quarantine channel
                    await quarantine.send(embed=embed_spammer(message.content))

                    # delete the messages
                    await self.bot.uber_last_message.delete()
                    await self.bot.last_message.delete()
                    await message.delete()

                # Else user is spamming one channel.
                else:
                    await message.author.timeout(
                        until=(datetime.now() + timedelta(seconds=30))
                        , reason="Spamming channels. Please refrain.")

        if is_second_message(message, self.last_message):
            self.uber_last_message = self.last_message

        self.last_message = message

        print(f"<{message.content} - {self.last_message.content} - {self.uber_last_message.content}")



def setup(bot):
    """
    Required.
    """
    bot.add_cog(ModerationSpamMessages(bot))
