"""
Once a user verifies, this cog is called.
"""
import discord
from discord.ext import commands
from cogs._settings import log_channel, mod_channel, normal_channel, user_roles  # pylint: disable=E0401


class AdminVerification(discord.ui.View):
    """
    We remove the needs approval role and send them a nice happy message.
    """
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify!", row=0, style=discord.ButtonStyle.success)
    async def verify_button_callback(self, interaction):
        """
        This is the stuff that happens
        - Send a nice happy message.
        """
        user = interaction.user
        guild = interaction.guild
        roles = guild.roles
        role = discord.utils.get(roles, id=user_roles["unverified"]["needs_approval"])

        website = "https://practical-python-org.github.io/Home/"
        website_emoji = discord.utils.get(self.bot.emojis, name="logo")
        email = "Practicalpython-staff@pm.me"
        email_emoji = "<:email:1040342884240597122>"
        review = "https://disboard.org/review/create/900302240559018015"
        review_emoji = "<:100:1040342353417863318>"
        created = str(guild.created_at.timestamp())
        created = created[:10]
        created_emoji = "<:triangular_flag_on_post:1040343017204228217>"
        owner = guild.owner.mention
        owner_emoji = discord.utils.get(self.bot.emojis, name="xarlos")
        invite = "https://discord.gg/vgZmgNwuHw"
        invite_emoji = "<:heart_hands:1040343137454915594>"

        quicklinks = f"{website_emoji} [Website]({website})" \
                     f"\n{email_emoji} {email}\n{review_emoji}" \
                     f" [Vote for us on disboard!]({review})"
        info = f"{created_emoji} Created: <t:{int(created)}:R>" \
               f"\n{owner_emoji} Owner: {owner}\n{invite_emoji} {invite}"

        embed = discord.Embed(
            title="Welcome to Practical Python", color=discord.Color.yellow()
        )
        embed.set_thumbnail(
            url="https://raw.githubusercontent.com/Xarlos89/PracticalPython/main/logo.png"
        )
        embed.add_field(
            name=f"You are member number {guild.member_count}!",
            value=f"""
            Awesome, {user.mention}. Thank you for verifying.
            Allow me to introduce you {guild.name}.
            
            1. Be sure to read our {self.bot.get_channel(mod_channel['rules_channel']).mention}.
            2. Set some roles using **/roles**
            3. Introduce yourself in {self.bot.get_channel(normal_channel['general_channel']).mention}.
            
            We keep a ton of awesome links to courses, cool tools, and popular software in {self.bot.get_channel(normal_channel['resources_channel']).mention}.
            If you have any questions, feel free to post your question in {self.bot.get_channel(normal_channel['python_help_1']).mention}
            
            I can run your code directly in the server!
            To learn how, type **/help** in any channel.
            
            Looking forward to having you here!
            """,
            inline=False,
        )
        embed.add_field(name="Quick Links", value=quicklinks)
        embed.add_field(name="Information", value=info)

        if "Needs Approval" in [role.name for role in user.roles]:
            await user.remove_roles(role)
            await user.send(embed=embed)

            log_channels = await self.bot.fetch_channel(
                log_channel["verification_log"]
            )  # ADMIN user log
            await log_channels.send(f"{user.mention} has verified!")

        else:
            await user.send("You have already been Verified. Go away.")


class VerifyHelper(commands.Cog):
    """
    this adds the button to the #verification channel so that people
    can verify
    TODO: Make this button persistent.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
    @commands.slash_command(
        description="Adds verify button to channel."
    )  # Create a slash command
    async def add_verify_button(self, ctx):
        """Adds the button"""
        await ctx.respond(
            "Please Verify that you are not a bot.", view=AdminVerification(self.bot)
            )

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
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
