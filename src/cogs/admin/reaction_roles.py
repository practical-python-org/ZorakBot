"""

This cog handles the /roles command.
It allows a user to call a dropdown that, when an option is selected, can
toggle a user's role.
"""
import os

import discord
import toml
from discord.ext import commands


ROLE_DATA = toml.load(os.path.join("Settings", "ReactionRoles.toml"))
reaction_roles = ROLE_DATA['reaction_roles']
selectors = ROLE_DATA['selectors']


async def remove_roles_if_exists(user, roles):
    """removes roles that a user has if the role exists on them"""
    for role in user.roles:
        if role in roles:
            await user.remove_roles(role)


class RoleDropdownSelector(discord.ui.Select):
    """
    This is the dropdown selection menu that the user interacts with.
    """
    def __init__(self, selector_data):
        self.name = selector_data['name']
        self.single_choice = selector_data['single_choice']
        self.description = selector_data['description']
        self.reaction_roles = selector_data['options']
        options = [
            discord.SelectOption(
                label=option["label"]
                , description=option["description"]
                , emoji=option["emoji"]
                , value=str(option["id"]
                            )
            )
            for option in self.reaction_roles
        ]
        options.append(
            discord.SelectOption(
                label="None"
                , description="Remove all roles"
                , emoji="❌"
                , value="0"
            )
        )
        super().__init__(placeholder=selector_data["description"], options=options)

    async def callback(self, interaction: discord.Interaction):
        """
        this is the fancy logic that does something on clicks.
        """
        selection = self.values[0]
        # selected_role gives back a nonetype when no roles are selected.
        # this is bad, because we error out when we select "no roles"
        # trying a ternary here to avoid it.
        selected_role = (discord.utils.get(
            interaction.guild.roles
            , id=int(selection)
        )) if selection != "0" else "0"

        roles = [
            discord.utils.get(
                interaction.guild.roles
                , id=option['id']
            )
            for option in self.reaction_roles
        ]

        # We add a second condition here to capture the event when
        # "remove all" is selected and a 0 is returned.
        if selected_role is not None or selection == "0":
            if selection == "0":
                await remove_roles_if_exists(interaction.user, roles)
                await interaction.response.send_message(
                    "Removed all roles in this group!"
                    , ephemeral=True
                )
            else:
                if selected_role.id in interaction.user.roles:
                    await interaction.user.remove_roles(selected_role)
                    await interaction.response.send_message(
                        f"Removed the <@&{selected_role.id}> role!"
                        , ephemeral=True
                    )
                else:
                    if self.single_choice:
                        await remove_roles_if_exists(interaction.user, roles)
                    await interaction.user.add_roles(selected_role)
                    await interaction.response.send_message(
                        f"Assigned the <@&{selected_role.id}> role!"
                        , ephemeral=True
                    )
        else:
            await interaction.response.send_message(
                "Role not found!"
                , ephemeral=True
            )


class SelectView(discord.ui.View):
    """
    This view allows us to construct a view with multiple other views
    under it. We also define our button timeout here.
    Consider this the entrypoint for all the other classes defined above.
    """

    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        for menu in selectors:
            self.add_item(RoleDropdownSelector(selectors[menu]))


class Roles(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """

    def __init__(self, bot):
        self.bot = bot  # Passed in from main.py

    # If you wanted to prepopulate the view with a user's current roles,
    # I think you could do it here. Grab the user object from ctx,
    # grab the roles, and pass it into the view. Which can then pass it into the dropdowns.
    @commands.slash_command(description="Get new roles, or change the ones you have!")
    async def roles(self, ctx):
        """The slash command that initiates the fancy menus."""
        await ctx.respond("Edit Reaction Roles", view=SelectView(), ephemeral=True)


def setup(bot):
    """
    Maszi likes to ruin parties.
    But Xarlos ERFORDERT REGELN UND STRUKTUR
    PASS AUF, ODER DU BEKOMMST DEN DEUTSCHEN DIKTATOR IN DEN GITHUB-KOMMENTAREN
    """
    bot.add_cog(Roles(bot))
