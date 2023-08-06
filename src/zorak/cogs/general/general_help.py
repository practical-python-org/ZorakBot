<<<<<<< HEAD:src/zorak/cogs/general/general_help.py
"""
this command creates a help button menu which includes
- Server info
- Running code
- code blocks
"""
import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class HelpButtons(discord.ui.View):
    """
    Here we create the button class for handling the helper.
    """

    def __init__(self, server_settings, *, timeout=None):
        super().__init__(timeout=timeout)
        self.server_settings = server_settings

=======
import discord
from discord.ext import commands
from cogs._settings import server_info


class helpButtons(discord.ui.View):
>>>>>>> Development:src/cogs/general/general_help.py
    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(label="Server Info", row=0, style=discord.ButtonStyle.success)
    async def first_button_callback(self, button, interaction):
        # FIXME This is never used
        # staff_role = interaction.guild.get_role(admin_roles["staff"])
        embed = discord.Embed(
<<<<<<< HEAD:src/zorak/cogs/general/general_help.py
            title=self.server_settings.server_info["name"],
            description=f"**- Website -**\n{self.server_settings.server_info['website']}\n\n"
            f" \**- Owner -**\n{interaction.guild.owner}\n\n"  # pylint: disable=W1401
            f" \**- Email -**\n{self.server_settings.server_info['email']}\n\n"  # pylint: disable=W1401
            f" \**- Invite Link -**\n{self.server_settings.server_info['invite']}\n\n"  # pylint: disable=W1401
            f" \**- Leave a reveiw -**\n{self.server_settings.server_info['review']}\n\n"  # pylint: disable=W1401
            f" \**- Questions? -**\nMake a ticket using /ticket, or"  # pylint: disable=W1401
            f" send us an email.",
=======
            title=server_info["name"],
            description=f"**- Website -**\n{server_info['website']}\n\n \
							**- Owner -**\n{interaction.guild.owner}\n\n \
							**- Email -**\n{server_info['email']}\n\n \
							**- Invite Link -**\n{server_info['invite']}\n\n \
							**- Leave a reveiw -**\n{server_info['review']}\n\n \
							**- Questions? -**\nMake a ticket using /ticket, or send us an email.",
>>>>>>> Development:src/cogs/general/general_help.py
            color=discord.Color.yellow(),
        )
        embed.set_thumbnail(url=self.server_settings.server_info["logo"])
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Running code", row=0, style=discord.ButtonStyle.success)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message(
            """To run python code in the chat, type:\n\n/run\n\`\`\`py\nx = 'hello world'\nprint(x)\n\`\`\`"""
        )

    @discord.ui.button(label="Code Blocks", row=0, style=discord.ButtonStyle.success)
    async def fourth_button_callback(self, button, interaction):
        await interaction.response.send_message(
            """To format your python code like this: ```py\nx = 'Hello World!'\n``` Type this: \n\`\`\`py\nYour code here\n\`\`\`"""
        )


<<<<<<< HEAD:src/zorak/cogs/general/general_help.py
class HelpCommand(commands.Cog):
    """
    This is the command (/help) that triggers our UI object to appear.
    """

=======
class helper(commands.Cog):
>>>>>>> Development:src/cogs/general/general_help.py
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ask Zorak for help.")
    async def help(self, ctx):
<<<<<<< HEAD:src/zorak/cogs/general/general_help.py
        """
        A standard slash command.
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)
        await ctx.respond("What do you want, human?", view=HelpButtons(self.bot.server_settings, timeout=120))
=======
        await ctx.respond("What do you want, human?", view=helpButtons(timeout=120))
>>>>>>> Development:src/cogs/general/general_help.py


def setup(bot):
    bot.add_cog(helper(bot))
