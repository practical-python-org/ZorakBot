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
from ._settings import logger, fun_roles, employment_roles


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
            discord.SelectOption(label="Beginner"
                                 , emoji="🟢"
                                 , description="Have little to no Python Experience"),
            discord.SelectOption(label="Intermediate"
                                 , emoji="🟡"
                                 , description="Can solve issues and diagnose problems"),
            discord.SelectOption(label="Professional"
                                 , emoji="🔴"
                                 , description="Using Python in professional life.")
        ]
        super().__init__(
            placeholder="Select your skill level!"
            , min_values=1, max_values=1
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
        relevant_roles = [
            fun_roles["beginner"]
            , fun_roles["intermediate"]
            , fun_roles["professional"]
        ]

        async def remove_role_if_exists(
                selected_role, target_role, all_members_roles
        ):
            """

            Args:
                selected_role: The role (string) selected in the dropdown menu.
                target_role: The selected role's object.
                all_members_roles: All roles that a member currently has. List of role IDs

            Returns:
                member.remove_roles
                interaction.response.send_message


            """
            if str(selected_role) in str(all_members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(target_role)
                logger.info(f'Removed {selection} from {member}.')
                await interaction.response.send_message(
                    f" - Removed role: <@&{selected_role}>"
                    , ephemeral=True
                )

        async def add_role_and_remove_others(
                selected_role, target_role, members_roles, all_relevant_roles
        ):
            """

            Args:
                selected_role: The role (string) that a user selected in the dropdown
                target_role: The selected role object.
                members_roles: All roles the user currently has. list of role IDs
                all_relevant_roles: The role IDs that are relevant in this role gorup

            Returns:
                member.add_roles
                interaction.response.send_message

            """
            if str(selected_role) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(target_role)
                logger.info(f'Added {selection} to {member}.')

                for role in all_relevant_roles:
                    if str(role) in str(members_roles):
                        await member.remove_roles(discord.utils.get(member.guild.roles, id=role))
                        logger.info(f'Removed {selection} from {member}.')
                        removals = f"{removals}\n - Removed: <@&{role}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{selected_role}>{removals}"
                    , ephemeral=True
                )

        if selection == 'beginner':
            await remove_role_if_exists(
                fun_roles[selection], beginner_role, members_roles)
            await add_role_and_remove_others(
                fun_roles[selection], beginner_role, members_roles, relevant_roles)
        elif selection == 'intermediate':
            await remove_role_if_exists(
                fun_roles[selection], intermediate_role, members_roles)
            await add_role_and_remove_others(
                fun_roles[selection], intermediate_role, members_roles, relevant_roles)
        elif selection == 'professional':
            await remove_role_if_exists(
                fun_roles[selection], professional_role, members_roles)
            await add_role_and_remove_others(
                fun_roles[selection], professional_role, members_roles, relevant_roles)


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
        and then the logic begins.
        We define two functions.

        remove_role_if_exists - Removes the selected role if a user has it.
        add_role_and_remove_others - If it does not exist, Add it, and remove
                                    any other that DOES exist in the role grouping.
        """
        member = interaction.user
        members_roles = member.roles
        selection = self.values[0].lower()
        north_america = discord.utils.get(member.guild.roles, id=fun_roles["north_america"])
        europe = discord.utils.get(member.guild.roles, id=fun_roles["europe"])
        asia = discord.utils.get(member.guild.roles, id=fun_roles["asia"])
        africa = discord.utils.get(member.guild.roles, id=fun_roles["africa"])
        south_america = discord.utils.get(member.guild.roles, id=fun_roles["south_america"])
        oceana = discord.utils.get(member.guild.roles, id=fun_roles["oceana"])
        relevant_roles = [
            fun_roles["north_america"]
            , fun_roles["europe"]
            , fun_roles["asia"]
            , fun_roles["africa"]
            , fun_roles["south_america"]
            , fun_roles["oceana"]
        ]

        async def remove_role_if_exists(
                selected_role, target_role, all_members_roles
        ):
            """

            Args:
                selected_role: The role (string) selected in the dropdown menu.
                target_role: The selected role's object.
                all_members_roles: All roles that a member currently has. List of role IDs

            Returns:
                member.remove_roles
                interaction.response.send_message


            """
            if str(selected_role) in str(all_members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(target_role)
                logger.info(f'Removed {selection} from {member}.')
                await interaction.response.send_message(
                    f" - Removed role: <@&{selected_role}>"
                    , ephemeral=True
                )

        async def add_role_and_remove_others(
                selected_role, target_role, members_roles, all_relevant_roles
        ):
            """

            Args:
                selected_role: The role (string) that a user selected in the dropdown
                target_role: The selected role object.
                members_roles: All roles the user currently has. list of role IDs
                all_relevant_roles: The role IDs that are relevant in this role gorup

            Returns:
                member.add_roles
                interaction.response.send_message

            """
            if str(selected_role) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(target_role)
                logger.info(f'Added {selection} to {member}.')

                for role in all_relevant_roles:
                    if str(role) in str(members_roles):
                        await member.remove_roles(discord.utils.get(member.guild.roles, id=role))
                        logger.info(f'Removed {selection} from {member}.')
                        removals = f"{removals}\n - Removed: <@&{role}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{selected_role}>{removals}"
                    , ephemeral=True
                )

        if selection == 'north america':
            selected_role = fun_roles[selection.replace(" ", "_")]
            await remove_role_if_exists(
                selected_role, north_america, members_roles)
            await add_role_and_remove_others(
                selected_role, north_america, members_roles, relevant_roles)
        elif selection == 'europe':
            await remove_role_if_exists(
                fun_roles[selection], europe, members_roles)
            await add_role_and_remove_others(
                fun_roles[selection], europe, members_roles, relevant_roles)
        elif selection == 'asia':
            await remove_role_if_exists(
                fun_roles[selection], asia, members_roles)
            await add_role_and_remove_others(
                fun_roles[selection], asia, members_roles, relevant_roles)
        elif selection == 'africa':
            await remove_role_if_exists(
                fun_roles[selection], africa, members_roles)
            await add_role_and_remove_others(
                fun_roles[selection], africa, members_roles, relevant_roles)
        elif selection == 'south america':
            selected_role = fun_roles[selection.replace(" ", "_")]
            await remove_role_if_exists(
                selected_role, south_america, members_roles)
            await add_role_and_remove_others(
                selected_role, south_america, members_roles, relevant_roles)
        elif selection == 'oceana':
            await remove_role_if_exists(
                fun_roles[selection], oceana, members_roles)
            await add_role_and_remove_others(
                fun_roles[selection], oceana, members_roles, relevant_roles)


class EmploymentRoles(discord.ui.Select):
    """
    This is the third box in the command.
    Our innit defines the button names and labels.
    TODO: Add values as a param in the discord.SelectOption,
            they can then be used in the callback.
            For example, the values can be the role.id, which
            would remove the need to extend the logic in the callback
    Then our callback is the response to when those button labels are clicked.
    """

    def __init__(self):
        options = [
            discord.SelectOption(label="Open to Work"
                                 , emoji="🛠️"
                                 , description="You are open to taking Python related jobs."),
            discord.SelectOption(label="Employer"
                                 , emoji="👩‍💼"
                                 , description="You are looking to hiring a Python developer."),
            ]
        super().__init__(
            placeholder="Are you open to work / Looking for a developer?!"
            , min_values=0, max_values=2
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
        selection = self.values

        async def add_or_remove_roles(selected_role, users_roles):
            """
            If a selected role exists on a user, remove it.
            If a selected role does not exist, add it.
            """
            role_name = selected_role.replace(" ", "_").lower()
            role_obj = discord.utils.get(
                member.guild.roles
                , id=employment_roles[role_name]
            )

            if str(employment_roles[role_name]) in str(users_roles):

                await member.remove_roles(role_obj)
                logger.info(f'Removed {selected_role} from {member}.')
                return f"- Removed role: <@&{employment_roles[role_name]}>\n"
            if str(employment_roles[role_name]) not in str(users_roles):
                await member.add_roles(role_obj)
                logger.info(f'Added {selected_role} to {member}.')
                return f"- Added role: <@&{employment_roles[role_name]}>\n"

        # add_or_remove_roles returns a string, stating what happened.
        message = ''
        for user_selected_roles in selection:
            message = message + await add_or_remove_roles(user_selected_roles, members_roles)

        if len(message) > 1: # This avoids an error where no role is added or removed.
            await interaction.response.send_message(message, ephemeral=True)


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
        self.add_item(EmploymentRoles())


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
