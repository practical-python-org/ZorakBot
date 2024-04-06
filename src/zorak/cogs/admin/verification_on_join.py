"""
This is a handler that adds a Need Approval role and sends the user a message.
"""
from asyncio import sleep
import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class LoggingVerification(commands.Cog):
    """
    Handled with a role, and a message.
    the role limits the user to one channel, with a verify button.
    If the user does not push the button within one hour, they are auto-kicked.
    """

    def __init__(self, bot):
        self.bot = bot

    async def log_unverified_join(self, member, logging_channel):
        await logging_channel.send(f"<@{member.id}> joined, but has not verified.")

    async def kick_if_not_verified(self, member, time_to_kick, logging_channel):
        await sleep(time_to_kick)

        if "✅" not in [role.name for role in member.roles]:
            await logging_channel.send(
                f"{member.mention} did not verify after {int((time_to_kick / 3600))} hour/s, auto-removed.")
            await member.kick(reason="Did not verify.")

    async def send_welcome_message(self, guild, member, settings):
        welcome_message = f"""
            Hi there, {member.mention}
            I'm Zorak, the moderator of {guild.name}.

            We are very happy that you have decided to join us.
            Before you are allowed to chat, you need to verify that you aren't a bot.
            Dont worry, it's easy. Just go to
            {self.bot.get_channel(settings.verification_channel).mention}
            and click the green button.

            After you do, all of {guild.name} is available to you. Have a great time :-)
            """
        # Send Welcome Message
        try:
            await member.send(welcome_message)
        except discord.errors.Forbidden as catch_dat_forbidden:
            logger.debug(f'{member.name} cannot be sent a DM.')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        settings = self.bot.db_client.get_guild_settings(member.guild)

        logs_channel = await self.bot.fetch_channel(settings["verification_log"])

        await self.log_unverified_join(member, logs_channel)
        await self.send_welcome_message(guild, member, settings)
        await self.kick_if_not_verified(member, 3600, logs_channel)


def setup(bot):
    """Required"""
    bot.add_cog(LoggingVerification(bot))


