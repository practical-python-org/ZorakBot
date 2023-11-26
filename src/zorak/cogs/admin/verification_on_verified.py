"""
Once a user verifies, this cog is called.
"""
import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

from zorak.utilities.cog_helpers._embeds import embed_verified_success  # pylint: disable=E0401


class AdminVerification(discord.ui.View):
    """
    We remove the needs approval role and send them a nice happy message.
    """

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    def is_verified(self, member):
        if "✅" in [role.name for role in member.roles]:
            return True
        
    async def send_wrong_button_message(self, guild, member):
        button_message = f"""
            Hi there, {member.mention}
            you have pressed the wrong button to verify yourself. 

            Make sure you press the **GREEN** button to verify yourself.
            Please join the server again and try again.
            {self.bot.server_settings.server_info['invite']}
            """
        # Send Welcome Message
        try:
            await member.send(button_message)
        except discord.errors.Forbidden as catch_dat_forbidden:
            logger.debug(f'{member.name} cannot be sent a DM caused by failing verify by pressing red button.')

    async def send_wrong_button_message_and_kick(self, interaction: discord.Interaction):
        """
        Sends a wrong button message and kicks the user.
        """
        user = interaction.user
        await self.send_wrong_button_message(interaction.guild, user)
        await user.kick(reason="User failed to verify by pressing red button.")

    @discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.red)
    async def verify_button_callback_red_1(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        This is a dummy button, if pressed kicks user.
        """
        await self.send_wrong_button_message_and_kick(interaction)

    @discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.red)
    async def verify_button_callback_red_2(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        This is a dummy button, if pressed kicks user.
        """
        await self.send_wrong_button_message_and_kick(interaction)

    @discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.success)
    async def verify_button_callback_green(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        This is the stuff that happens
        - Send a nice happy message.
        """
        user = interaction.user
        verified = self.is_verified(user)
        # Moved this up here, as someone "unverified" might be able to block the command.
        if verified:
            await user.send("You have already been Verified. Go away.")
            return

        embed = discord.Embed(title="Welcome to Practical Python", color=discord.Color.yellow())
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Xarlos89/PracticalPython/main/logo.png")

        if not verified:
            guild = interaction.guild
            roles = guild.roles
            try:
                await user.send(embed=embed)
            except discord.errors.Forbidden:
                logger.debug(f'{user.name} cannot be sent a DM for verification confirmation.')

            verified_role = discord.utils.get(roles, id=self.bot.server_settings.verified_role['verified'])
            await user.add_roles(verified_role)

            log_channels_verification_log = await self.bot.fetch_channel(self.bot.server_settings.log_channel["verification_log"])
            log_channels_join = await self.bot.fetch_channel(self.bot.server_settings.log_channel["join_log"])

            await log_channels_verification_log.send(f"{user.mention} has verified!")
            await log_channels_join.send(embed=embed_verified_success(user.mention, user.guild.member_count))

    @discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.red)
    async def verify_button_callback_red_3(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        This is a dummy button, if pressed kicks user.
        """
        await self.send_wrong_button_message_and_kick(interaction)

    @discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.red)
    async def verify_button_callback_red_4(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        This is a dummy button, if pressed kicks user.
        """
        await self.send_wrong_button_message_and_kick(interaction)


class VerifyHelper(commands.Cog):
    """
    this adds the button to the #verification channel so that people
    can verify
    TODO: Make this button persistent.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
    @commands.slash_command(description="Adds verify button to channel.")  # Create a slash command
    async def add_verify_button(self, ctx):
        """Adds the button"""
        button_message = ("Welcome to Practical Python! We’re thrilled to have you here to learn "
                          "and collaborate with fellow Python enthusiasts. Before diving in, "
                          "please click the **GREEN** 'Verify' button to confirm your identity and gain "
                          "access to the server. **If you click the RED button you will be kicked!** Feel free to introduce yourself and don't "
                          "hesitate to ask any questions. Happy coding!")
        
        await ctx.respond(button_message, view=AdminVerification(self.bot))

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"Sorry, {ctx.author.name}, you dont have permission to use this command!",
                reference=ctx.message,
            )
        else:
            raise error


def setup(bot):
    """Required."""
    bot.add_cog(VerifyHelper(bot))
