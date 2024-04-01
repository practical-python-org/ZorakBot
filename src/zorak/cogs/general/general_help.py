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

    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(label="Server Info", row=0, style=discord.ButtonStyle.success)
    async def first_button_callback(self, button, interaction):
        # staff_role = interaction.guild.get_role(admin_roles["staff"])
        embed = discord.Embed(
            title=f"{self.server_settings.info['name']}",
            description=f"**Website** \n{self.server_settings.info['website']}\n\n"
            f"**Owner** \n{interaction.guild.owner.mention}\n\n"  # pylint: disable=W1401
            f"**Email** \n{self.server_settings.info['email']}\n\n"  # pylint: disable=W1401
            f"**Invite Link** \n{self.server_settings.info['invite']}\n\n"  # pylint: disable=W1401
            f"**Leave a reveiw** \n{self.server_settings.info['review']}\n\n"  # pylint: disable=W1401
            f"**Questions?** \nMake a ticket using **/ticket**, or send us an email.",
            color=discord.Color.yellow(),
        )
        embed.set_thumbnail(url=self.server_settings.info["logo"])
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


class HelpCommand(commands.Cog):
    """
    This is the command (/help) that triggers our UI object to appear.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ask Zorak for help.")
    async def help(self, ctx):
        """
        A standard slash command.
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)
        await ctx.respond("What do you want, human?", view=HelpButtons(self.bot.settings, timeout=120))


def setup(bot):
    bot.add_cog(HelpCommand(bot))
