"""
A listener that looks for repeat messages and destroys them.
"""
import logging
from datetime import datetime, timedelta

import discord.errors
from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import (
    embed_spammer,  # pylint: disable=E0401
    embed_spammer_warn  # pylint: disable=E0401
)


logger = logging.getLogger(__name__)


class ModerationSpamMessages(commands.Cog):
    """
    Destroying spam with bots
    """

    def __init__(self, bot):
        self.bot = bot
        self.records = {}
        self.warn_message = 'Hello there!'

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Scans every message and compares them
        """

        # Dont catch Zorak
        if message.author.bot:
            return

        # new speaker. Welcome to auto mod.
        if message.author.id not in self.records:
            self.records[message.author.id] = {
                "last_message": message.content
                , "occurrence": 1
                , "1st": {"message_id": message.id, "channel_id": message.channel.id}
                , "2nd": {}
                , "3rd": {}
            }

        # Old speaker. We are watching you...
        else:
            # Check if the last message is the same as the new one.
            the_archive = self.records[message.author.id]

            if the_archive["last_message"] == message.content:
                # If so, increase the occurance by 1
                the_archive["occurrence"] += 1
                logger.debug("%s has sent a double message in %s", message.author.name, message.channel.name)

                if the_archive["occurrence"] == 2:
                    # when a repeat message is sent, set the message ID for the 2nd message
                    the_archive["2nd"]["message_id"] = message.id
                    the_archive["2nd"]["channel_id"] = message.channel.id

                    if the_archive["1st"]["channel_id"] != the_archive["2nd"]["channel_id"]:
                        await message.author.timeout(until=datetime.utcnow() + timedelta(seconds=15))
                        logger.info("%s was timed out (2/3 messages)", message.author.name)
                        channel1 = await self.bot.fetch_channel(the_archive["1st"]["channel_id"])
                        channel2 = await self.bot.fetch_channel(the_archive["2nd"]["channel_id"])

                        # Send a DM. If you can't, send in the channel.
                        try:
                            await message.author.send(embed=embed_spammer_warn(channel1, channel2))
                            logger.debug("%s was sent a DM about their double message.", message.author.name)
                        except discord.errors.HTTPException as closed_dms:
                            logger.debug("could not send %s a message, diverting to channel: %s"
                                         , message.author.name
                                         , message.channel.name)

                            first_channel = await self.bot.fetch_channel(the_archive['1st']['channel_id'])
                            self.warn_message = await message.reply(
                                f"{message.author.mention}, Please do not post the same message in "
                                f"multiple channels.\n You already posted this in {first_channel.mention}")

                if the_archive["occurrence"] == 3:
                    # You lost the game, asshole.
                    logger.info("%s was quarantined for sending 3 repeat messages.", message.author.name)
                    the_archive["3rd"]["message_id"] = message.id
                    the_archive["3rd"]["channel_id"] = message.channel.id

                    # timeout right away
                    await message.author.timeout(until=datetime.utcnow() + timedelta(seconds=30))

                    naughty = message.author.guild.get_role(self.bot.server_settings.user_roles["bad"]["naughty"])
                    verified = message.author.guild.get_role(self.bot.server_settings.verified_role['verified'])
                    quarantine = await self.bot.fetch_channel(
                        self.bot.server_settings.channels["moderation"]["quarantine_channel"])

                    # assign Naughty roll
                    member = message.author
                    await member.remove_roles(verified)
                    await member.add_roles(naughty)

                    # Post the message in Quarantine channel
                    await quarantine.send(embed=embed_spammer(message.content))

                    # delete the messages
                    channel1 = await self.bot.fetch_channel(the_archive["1st"]["channel_id"])
                    channel2 = await self.bot.fetch_channel(the_archive["2nd"]["channel_id"])
                    channel3 = await self.bot.fetch_channel(the_archive["3rd"]["channel_id"])

                    one = await channel1.fetch_message(the_archive["1st"]["message_id"])
                    two = await channel2.fetch_message(the_archive["2nd"]["message_id"])
                    three = await channel3.fetch_message(the_archive["3rd"]["message_id"])
                    await one.delete()
                    await two.delete()
                    await three.delete()
                    await self.warn_message.delete()

                    # reset after the quarantine, as the user might actually not be a bot.
                    self.records[message.author.id] = {
                        "last_message": message.content
                        , "occurrence": 1
                        , "1st": {"message_id": message.id, "channel_id": message.channel.id}
                        , "2nd": {}
                        , "3rd": {}
                    }

            else:
                # Message is new, and we reset back to the first occurrence.
                self.records[message.author.id] = {
                    "last_message": message.content
                    , "occurrence": 1
                    , "1st": {"message_id": message.id, "channel_id": message.channel.id}
                    , "2nd": {}
                    , "3rd": {}
                }

        # For debugging
        # print(self.records[message.author.id])


def setup(bot):
    """
    Required.
    """
    bot.add_cog(ModerationSpamMessages(bot))
