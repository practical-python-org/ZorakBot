"""
This cog allows us to create tickets.
"""
import logging

import discord
from discord.ext import commands




logger = logging.getLogger(__name__)


class AddTicketButton(commands.Cog):
    """
    This is the slash command that sends our UI element.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ticket(self, ctx):
        """
        A simple command with a view.
        """
        settings = self.bot.db_client.get_guild_settings(ctx.guild)
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)
        await ctx.respond(
            "Do you need help, or do you have a question for the Staff?",
            view=MakeATicket(settings),
            ephemeral=True,
        )


class MakeATicket(discord.ui.View):
    """
    A UI component that sends a button, which does other things.
    """

    def __init__(self, settings, *, timeout=None):
        super().__init__(timeout=timeout)
        self.settings = settings

    @discord.ui.button(label="Open a support Ticket", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        """
        The callback on the button, or... what happens on click.
        """
        await interaction.response.defer()
        button.label = "Ticket Created!"
        button.disabled = True
        await interaction.edit_original_response(view=self)

        support = await interaction.guild.fetch_channel(self.settings["support_channel"])
        staff = interaction.guild.get_role(self.settings["staff_role"])

        ticket = await support.create_thread(
            name=f"[Ticket] - {interaction.user}",
            message=None,
            auto_archive_duration=4320,
            type=discord.ChannelType.private_thread,
            reason=None,
        )

        # TODO: Can just mention the staff role here instead of a for loop
        for person in interaction.guild.members:
            if staff in person.roles:
                await ticket.add_user(person)

        await ticket.add_user(interaction.user)
        await ticket.send(f"**{interaction.user.mention}, we have received your ticket.**")
        await ticket.send("To better help you, please describe your issue.")


def setup(bot):
    """
    Required
    """
    bot.add_cog(AddTicketButton(bot))
