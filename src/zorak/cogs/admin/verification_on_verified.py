"""

This cog handles the /roles command.
It allows a user to call a dropdown that,
when an option is selected, can verify or kick the user

"""
import logging
from random import shuffle
import discord
from discord.ext import commands
from time import sleep

from zorak.utilities.cog_helpers._embeds import embed_verified_success  # pylint: disable=E0401


logger = logging.getLogger(__name__)


class VerificationSelector(discord.ui.Select):
    """
    This is the dropdown selection menu that the user interacts with.
    """

    def __init__(self, discord_bot, selector_data):
        self.bot = discord_bot
        self.name = selector_data["name"]
        self.single_choice = selector_data["single_choice"]
        self.description = selector_data["description"]
        self.verification_options = selector_data["options"]
        options = [
            discord.SelectOption(label=option["label"], description=option["description"], emoji=option["emoji"],
                                 value=str(option["id"]))
            for option in self.verification_options
        ]

        super().__init__(placeholder=selector_data["description"], options=options)

    async def send_wrong_button_message(self, guild, member):
        try:
            await member.send(
                f"""
                Hi there, {member.mention}
                you have selected the wrong button.

                ** _Make sure you press the "Verify me!" button to verify yourself._ **

                Please join the server again and try again.
                {self.bot.server_settings.server_info['invite']}
                """
            )
        except discord.errors.Forbidden as catch_dat_forbidden:
            logger.info(f'Tried to send re-verify message but {member.name} cannot be sent a DM')

    async def send_wrong_button_message_and_kick(self, interaction: discord.Interaction):
        """
        Sends a wrong button message and kicks the user.
        """
        user = interaction.user
        await self.send_wrong_button_message(interaction.guild, user)
        await user.kick(reason="User failed to verify by admitting you are a robot. Fool.")

    async def callback(self, interaction: discord.Interaction):
        """
        this is the fancy logic that does something on clicks.
        """
        selection = self.values[0]
        selected_role = (discord.utils.get(interaction.guild.roles, id=int(selection))) if selection != "0" else "0"

        roles = [discord.utils.get(interaction.guild.roles, id=option["id"]) for option in self.verification_options]

        # We add a second condition here to capture the event when
        # "remove all" is selected and a 0 is returned.
        if selected_role is not None:

            if selection in ["0", "1", "2", "3", "4", "5"]:
                # One day, i'll fix this. But not today.
                # Instead of a role ID, to kick, we just send 0,1,2,3,4,5 for the kick buttons.
                logger.info("User clicked the wrong verification button, attempting to reach out.")
                await interaction.response.send_message("You're a robot?? BEGONE.", ephemeral=True)
                sleep(5)  # Let them read the "I'm gonna kick u" message.
                await self.send_wrong_button_message_and_kick(interaction)

            else:
                try:
                    if self.single_choice:
                        await interaction.user.add_roles(selected_role)
                        logger.info(f"{interaction.user.display_name} has verified!")

                        # Fetch channels AFTER role add, so broken config doesn't break verification.
                        log_channels_join = await self.bot.fetch_channel(
                            self.bot.server_settings.log_channel["join_log"])
                        logs_channel_verify = await self.bot.fetch_channel(
                            self.bot.server_settings.log_channel["verification_log"])

                        await interaction.response.send_message(
                            f"You have been verified!: <@&{selected_role.id}>", ephemeral=True)
                        await logs_channel_verify.send(f"<@{interaction.user.id}> joined, but has not verified.")
                        await log_channels_join.send(
                            embed=embed_verified_success(
                                interaction.user.mention
                                , interaction.user.guild.member_count
                            )
                        )
                except Exception as shit:
                    logger.info(f"Attempted to verify someone...\nERROR: {shit}")
        else:
            logger.warning("If you see this message... ")
            await interaction.response.send_message("Role not found!", ephemeral=True)


class SelectView(discord.ui.View):
    """
    This view allows us to construct a view with multiple other views
    under it. We also define our button timeout here.
    Consider this the entrypoint for all the other classes defined above.
    """
    def __init__(self, bot, verification_data, *, timeout=180):
        super().__init__(timeout=timeout)
        selectors = verification_data["selectors"]
        shuffle(selectors)
        for menu in selectors:
            self.add_item(VerificationSelector(bot, selectors[menu]))


class Verification(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """

    def __init__(self, bot):
        self.bot = bot  # Passed in from main.py

    # If you wanted to prepopulate the view with a user's current roles,
    # I think you could do it here. Grab the user object from ctx,
    # grab the roles, and pass it into the view. Which can then pass it into the dropdowns.
    @commands.slash_command(description="Verification!")
    async def verify(self, ctx):
        """The slash command that initiates the fancy menus."""
        if hasattr(self.bot.server_settings, "verification_options"):
            if "selectors" in self.bot.server_settings.verification_options:
                if "✅" not in [role.name for role in ctx.author.roles]:
                    await ctx.respond(
                        "# ~ Verification ~ \n"
                        "_Before you can join the server, we need to make sure you are not a robot._\n"
                        "_Please answer the following question._"
                        , view=SelectView(self.bot, self.bot.server_settings.verification_options)
                        , ephemeral=True
                    )
                else:
                    await ctx.respond("You are already verified. Go away.", ephemeral=True)
            else:
                await ctx.respond(
                    "Please contact the @Staff. Verification is having technical problems."
                    , ephemeral=True
                )
        else:
            await ctx.respond("Verification has not been set up!", ephemeral=True)


def setup(bot):
    bot.add_cog(Verification(bot))
