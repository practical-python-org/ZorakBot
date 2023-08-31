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

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """On join, do this stuff."""
        # Add verification role
        await member.add_roles(member.guild.get_role(self.bot.server_settings.unverified_role["needs_approval"]))

        # Log unverified join
        logs_channel = await self.bot.fetch_channel(
            self.bot.server_settings.log_channel["verification_log"])  # ADMIN user log
        await logs_channel.send(f"<@{member.id}> joined, but has not verified.")

        # Send Welcome
        guild = member.guild
        welcome_message = f"""
Hi there, {member.mention}
I'm Zorak, the moderatior of {guild.name}.

We are very happy that you have decided to join us.
Before you are allowed to chat, you need to verify that you aren't a bot.
Dont worry, it's easy. Just go to 
{self.bot.get_channel(self.bot.server_settings.mod_channel['verification_channel']).mention}
and click the green button.

After you do, all of {guild.name} is availibe to you. Have a great time :-)
"""
        # Send Welcome Message
        try:
            await member.send(welcome_message)
        except discord.errors.Forbidden as catch_dat_forbidden:
            logger.debug(f'{member.name} cannot be sent a DM.')

        time_unverified_kick = 3600  # 1 hour
        await sleep(time_unverified_kick)

        # Start verification timer
        if "Needs Approval" in [role.name for role in member.roles]:
            # Kick timer, in seconds.
            time_unverified_kick = 3600  # 1 hour
            await sleep(time_unverified_kick)

            if "Needs Approval" in [role.name for role in member.roles]:
                # Log the kick
                await logs_channel.send(
                    f"{member.mention} did not verify, auto-removed." f" ({(time_unverified_kick / 3600)} hour/s)")
                await member.kick(reason="Did not verify.")


def setup(bot):
    """Required"""
    bot.add_cog(LoggingVerification(bot))
