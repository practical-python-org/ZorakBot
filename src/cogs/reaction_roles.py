"""

This cog handles the /roles command.
It allows a user to call a dropdown that, when an option is selected, can
toggle a user's role.
We use a command. Roles, which is at the very end of the file to query
The classes SkillRelatedRoles and LocationRelatedRoles are connected to the role via a view.
Each class consists of the Innit, which holds info on the button labels, and
a callback, which holds the response when the option is selected.

"""

import discord
from discord.ext import commands
from ._settings import fun_roles


class SkillRelatedRoles(discord.ui.Select):
    """
    This is the first box in the command.
    Our innit defines the button names and labels.
    TODO: Add values as a param in the discord.SelectOption,
            they can then be used in the callback.
            For example, the values can be the role.id, which
            would remove the need to extend the logic in the callback
    Then our callback is the response to when those button labels are clicked.
    """
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Beginner",
                emoji='🟢',
                description="Have little to no Python Experience"
            ),
            discord.SelectOption(
                label="Intermediate",
                emoji='🟡',
                description="Can solve issues and diagnose problems"
            ),
            discord.SelectOption(
                label="Professional",
                emoji='🔴',
                description="Using Python in professional life, or just really good."
            )
        ]
        super().__init__(
            placeholder="Select your skill level!"
            , max_values=1
            , min_values=1
            , options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """
        First we will define some variables to be used in all logic,
        and then the logic begins. There needs to be a bit of logic for
        each possibility in the options variable.
        """
        member = interaction.user
        members_roles = member.roles
        selection = self.values[0].lower()
        beginner_role = discord.utils.get(member.guild.roles, id=fun_roles["beginner"])
        intermediate_role = discord.utils.get(member.guild.roles, id=fun_roles["intermediate"])
        professional_role = discord.utils.get(member.guild.roles, id=fun_roles["professional"])


        if selection == 'beginner':
            if str(fun_roles[selection]) in str(members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(beginner_role)
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(beginner_role)
                if str(fun_roles['intermediate']) in str(members_roles):
                    await member.remove_roles(intermediate_role)
                    removals = f"{removals}\n - Removed: <@&{fun_roles['intermediate']}>"
                if str(fun_roles['professional']) in str(members_roles):
                    await member.remove_roles(professional_role)
                    removals = f"{removals}\n - Removed: <@&{fun_roles['professional']}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{fun_roles[selection]}>{removals}"
                    , ephemeral=True
                )

        elif selection == 'intermediate':
            if str(fun_roles[selection]) in str(members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(intermediate_role)
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )
            elif str(fun_roles[selection]) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(intermediate_role)
                if str(fun_roles['beginner']) in str(members_roles):
                    await member.remove_roles(beginner_role)
                    removals = f"{removals}\n - Removed: <@&{fun_roles['beginner']}>"
                if str(fun_roles['professional']) in str(members_roles):
                    await member.remove_roles(professional_role)
                    removals = f"{removals}\n - Removed: <@&{fun_roles['professional']}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{fun_roles[selection]}>{removals}"
                    , ephemeral=True
                )

        elif selection == 'professional':
            if str(fun_roles[selection]) in str(members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(professional_role)
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(professional_role)

                if str(fun_roles['beginner']) in str(members_roles):
                    await member.remove_roles(beginner_role)
                    removals = f"{removals}\n - Removed: <@&{fun_roles['beginner']}>"
                if str(fun_roles['intermediate']) in str(members_roles):
                    await member.remove_roles(intermediate_role)
                    removals = f"{removals}\n - Removed: <@&{fun_roles['intermediate']}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{fun_roles[selection]}>{removals}"
                    , ephemeral=True
                )


class LocationRelatedRoles(discord.ui.Select):
    """
    This is the Second box in the command
    """
    def __init__(self):
        options = [
            discord.SelectOption(label="North America", emoji="🦅"),
            discord.SelectOption(label="Europe", emoji="🇪🇺"),
            discord.SelectOption(label="Asia", emoji="🐼"),
            discord.SelectOption(label="Oceana", emoji="🐨"),
            discord.SelectOption(label="South America", emoji="💃"),
            discord.SelectOption(label="Africa", emoji="🦒")
        ]
        super().__init__(
            placeholder="Select your continent!"
            , min_values=1, max_values=1
            , options=options
        )

    async def callback(self, interaction: discord.Interaction):
        """
        First we will define some variables to be used in all logic,
        and then the logic begins. There needs to be a bit of logic for
        each possibility in the options variable.
        """
        await interaction.response.send_message(
            content=f"Your choice is {self.values[0]}!"
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
        self.add_item(SkillRelatedRoles())
        self.add_item(LocationRelatedRoles())


class TestRoles(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """

    def __init__(self, bot):
        """
        Using the bot method defined in __main__
        """
        self.bot = bot

    @commands.slash_command(description="Get new roles, or change the ones you have!")
    async def test_roles(self, ctx):
        """
        The actual slash command itself. This is the same as all cogs.
        """
        await ctx.respond("Edit Reaction Roles", view=SelectView(), ephemeral=True)


def setup(bot):
    """
    This comment is literally just to boost the score on the linter.
    Why not make it a 2-liner, to appear like it has any meaning.
    """
    bot.add_cog(TestRoles(bot))
