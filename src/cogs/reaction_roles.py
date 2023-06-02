import discord
from discord.ext import commands
from ._settings import fun_roles


class Skill(discord.ui.Select):
    """
    This is the first box in the command
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
        super().__init__(placeholder="Select your skill level!", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        """
                Define some things we use all over the place.
                """
        member = interaction.user
        members_roles = interaction.user.roles
        selection = self.values[0].lower()
        beginner_role = discord.utils.get(member.guild.roles, id=fun_roles["beginner"])
        intermediate_role = discord.utils.get(member.guild.roles, id=fun_roles["intermediate"])
        professional_role = discord.utils.get(member.guild.roles, id=fun_roles["professional"])

        """
        Start some logic
        """
        if selection == 'beginner':
            if str(fun_roles[selection]) in str(members_roles):
                """
                If the role exists on the person, simply remove it.
                """
                await member.remove_roles(beginner_role)
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                """
                If the role is NOT in the users roles, add it, and 
                remove the other related roles if they exist. 
                """
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
                """
                If the role exists on the person, simply remove it.
                """
                await member.remove_roles(intermediate_role)
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                """
                If the role is NOT in the users roles, add it, and 
                remove the other related roles if they exist. 
                """
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
                """
                If the role exists on the person, simply remove it.
                """
                await member.remove_roles(professional_role)
                await interaction.response.send_message(
                    f" - Removed role: <@&{fun_roles[selection]}>"
                    , ephemeral=True
                )

            elif str(fun_roles[selection]) not in str(members_roles):
                """
                If the role is NOT in the users roles, add it, and 
                remove the other related roles if they exist. 
                """
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


class Location(discord.ui.Select):
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
        super().__init__(placeholder="Select your continent!", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Your choice is {self.values[0]}!", ephemeral=True)


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Skill())
        self.add_item(Location())


class TestRoles(commands.Cog):
    """
    This is the class that defines the actual slash command.
    It uses the view above to execute actual logic.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Get new roles, or change the ones you have!")
    async def test_roles(self, ctx):
        await ctx.respond("Edit Reaction Roles", view=SelectView(), ephemeral=True)


def setup(bot):
    bot.add_cog(TestRoles(bot))
