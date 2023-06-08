"""

This cog handles the /roles command.
It allows a user to call a dropdown that, when an option is selected, can
toggle a user's role.
"""
import os

import discord
import toml
from discord.ext import commands

from ._settings import logger

ROLE_DATA = toml.load(os.path.join(os.path.dirname(__file__), "..", "Resources", "ReactionRoles.toml"))


class RoleDropdownSelector(discord.ui.Select):
    def __init__(self, selector_data, roll_ids):
        self.name = selector_data["name"]
        self.role_ids = roll_ids
        options = [
            discord.SelectOption(label=option["label"], description=option["description"], emoji=option["emoji"], value=str(option["id"]))
            for option in selector_data["options"]
        ]
        super().__init__(placeholder=selector_data["description"], options=options)

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0].lower().replace(" ", "_")
        role = discord.utils.get(interaction.guild.roles, id=self.role_ids[f"{self.name}"][selection])
        if role is not None:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f"Removed the {role.name} role!", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Assigned the {role.name} role!", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found!", ephemeral=True)


class SelectView(discord.ui.View):
    """
    This view allows us to construct a view with multiple other views
    under it. We also define our button timeout here.
    Consider this the entrypoint for all the other classes defined above.
    """

    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        role_ids = ROLE_DATA["reaction_roles"]
        for selector in ROLE_DATA["selectors"]:
            self.add_item(RoleDropdownSelector(selector, role_ids))


class Roles(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """

    def __init__(self, bot):
        self.bot = bot  # Passed in from main.py

    @commands.slash_command(description="Get new roles, or change the ones you have!")
    async def roles(self, ctx):  # The ctx is passed in from the slash command.
        await ctx.respond("Edit Reaction Roles", view=SelectView(), ephemeral=True)


def setup(bot):
    """
    Xarlos likes to raise his linting score.
    I like to ruin parties.
    """
    bot.add_cog(Roles(bot))
