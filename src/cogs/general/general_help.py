"""
this command creates a help button menu which includes
- Server info
- Running code
- code blocks
"""
import logging
import discord
from discord.ext import commands
from cogs._settings import server_info  # pylint: disable=E0401


logger = logging.getLogger(__name__)


class HelpButtons(discord.ui.View):
    """
    Here we create the button class for handling the helper.
    """
    async def on_timeout(self):
        """
        Makes sure the buttons timeout with the command.
        """
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(label="Server Info", row=0, style=discord.ButtonStyle.success)
    async def first_button_callback(self, interaction):
        """
        the button for the Server info.
        """
        embed = discord.Embed(
            title=server_info["name"],
            description=f"**- Website -**\n{server_info['website']}\n\n"
                        f" \**- Owner -**\n{interaction.guild.owner}\n\n"  # pylint: disable=W1401
                        f" \**- Email -**\n{server_info['email']}\n\n"  # pylint: disable=W1401
                        f" \**- Invite Link -**\n{server_info['invite']}\n\n"  # pylint: disable=W1401
                        f" \**- Leave a reveiw -**\n{server_info['review']}\n\n"  # pylint: disable=W1401
                        f" \**- Questions? -**\nMake a ticket using /ticket, or"  # pylint: disable=W1401
                        f" send us an email.",
            color=discord.Color.yellow(),
        )
        embed.set_thumbnail(url=server_info["logo"])
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Running code", row=0, style=discord.ButtonStyle.success)
    async def second_button_callback(self, interaction):
        """
        this is the button for running code.
        """
        await interaction.response.send_message(
            "To run python code in the chat,"
            " type:\n\n/run\n\`\`\`py\nx = "  # pylint: disable=W1401
            "'hello world' \nprint(x) \`\`\`"  # pylint: disable=W1401
        )

    @discord.ui.button(label="Code Blocks", row=0, style=discord.ButtonStyle.success)
    async def third_button_callback(self, interaction):
        """
        this is the button for code blocks.
        """
        await interaction.response.send_message(
            "To format your python code like this:"
            " \n```py x = 'Hello World!' ``` Type "  # pylint: disable=W1401
            "this: \`\`\`py Your code here \`\`\`"  # pylint: disable=W1401
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
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        await ctx.respond("What do you want, human?", view=HelpButtons(timeout=120))


def setup(bot):
    """
    Required.
    """
    bot.add_cog(HelpCommand(bot))
