"""
Once a user verifies, this cog is called.
"""
import discord
from discord.ext import commands


class AdminVerification(discord.ui.View):
    """
    We remove the needs approval role and send them a nice happy message.
    """

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    async def is_verified(self, member):
        if "✅" in [role.name for role in member.roles]:
            return True

    @discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.success)
    async def verify_button_callback(self, bot, interaction):
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
            await user.send(embed=embed)
            verified_role = discord.utils.get(roles, id=self.bot.server_settings.verified['verified'])
            await user.add_roles(verified_role)
            log_channels = await self.bot.fetch_channel(self.bot.server_settings.log_channel["verification_log"])
            await log_channels.send(f"{user.mention} has verified!")


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
                          "please click the 'Verify' button to confirm your identity and gain "
                          "access to the server. Feel free to introduce yourself and don't "
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
