"""
This cog handles reaction roles.
Not sure how to handle multiple role-sets yet.
 - New cog?
 - New class?
"""
import discord
from discord.ext import commands
from ._settings import fun_roles


class RoleMenu(discord.ui.View):
    """
    This is the logic for the reaction roles.
    It holds the dropdown in the @discord.ui.select
    And then the logic inside the select_callback()
    """
    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)

    @discord.ui.select(
        placeholder="What is your skill level?",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Beginner",
                description="Have little to no Python Experience"
            ),
            discord.SelectOption(
                label="Intermediate",
                description="Can solve issues and diagnose problems"
            ),
            discord.SelectOption(
                label="Professional",
                description="Using Python in professional life, or just really good."
            )
        ]
    )
    async def select_callback(self, select, interaction):
        """
        Define some things we use all over the place.
        """
        member = interaction.user
        members_roles = interaction.user.roles
        selection = select.values[0].lower()

        beginner_role = discord.utils.get(
            member.guild.roles, id=fun_roles["beginner"]
        )
        intermediate_role = discord.utils.get(
            member.guild.roles, id=fun_roles["intermediate"]
        )
        professional_role = discord.utils.get(
            member.guild.roles, id=fun_roles["professional"]
        )

        if selection == 'beginner':
            if str(fun_roles[selection]) in str(members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(
                    beginner_role
                )
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(
                    beginner_role
                )
                if str(fun_roles['intermediate']) in str(members_roles):
                    await member.remove_roles(
                        intermediate_role
                    )
                    removals = f"{removals}\n - Removed: <@&{fun_roles['intermediate']}>"

                if str(fun_roles['professional']) in str(members_roles):
                    await member.remove_roles(
                        professional_role
                    )
                    removals = f"{removals}\n - Removed: <@&{fun_roles['professional']}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{fun_roles[selection]}>{removals}"
                    , ephemeral=True
                )

        elif selection == 'intermediate':
            if str(fun_roles[selection]) in str(members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(
                    intermediate_role
                )
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(
                    intermediate_role
                )
                if str(fun_roles['beginner']) in str(members_roles):
                    await member.remove_roles(
                        beginner_role
                    )
                    removals = f"{removals}\n - Removed: <@&{fun_roles['beginner']}>"
                if str(fun_roles['professional']) in str(members_roles):
                    await member.remove_roles(
                        professional_role
                    )
                    removals = f"{removals}\n - Removed: <@&{fun_roles['professional']}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{fun_roles[selection]}>{removals}"
                    , ephemeral=True
                )
        elif selection == 'professional':
            if str(fun_roles[selection]) in str(members_roles):
                # If the role exists on the person, simply remove it.
                await member.remove_roles(
                    professional_role
                )
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                # If the role is NOT in the users roles, add it, and
                # remove the other related roles if they exist.
                removals = ''
                await member.add_roles(
                    professional_role
                )

                if str(fun_roles['beginner']) in str(members_roles):
                    await member.remove_roles(
                        beginner_role
                    )
                    removals = f"{removals}\n - Removed: <@&{fun_roles['beginner']}>"
                if str(fun_roles['intermediate']) in str(members_roles):
                    await member.remove_roles(
                        intermediate_role
                    )
                    removals = f"{removals}\n - Removed: <@&{fun_roles['intermediate']}>"

                await interaction.response.send_message(
                    f" - Added role: <@&{fun_roles[selection]}>{removals}"
                    , ephemeral=True
                )


class ReactionRoles(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Get new roles, or change the ones you have!")
    async def roles(self, ctx):
        """
        This is the main entrypoint for the cog
        """
        await ctx.respond(
            "Edit Reaction Roles"
            , view=RoleMenu(timeout=180)
            , ephemeral=True
        )


def setup(bot):
    """
    This comment is literally just to chill the linter out.
    """
    bot.add_cog(ReactionRoles(bot))
