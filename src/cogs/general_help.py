import discord
from discord.ext import commands
from ._settings import server_info


class helpButtons(discord.ui.View):
    async def on_timeout(self):
        for button in self.children:
            button.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(label="Server Info", row=0, style=discord.ButtonStyle.success)
    async def first_button_callback(self, button, interaction):
        # FIXME This is never used
        # staff_role = interaction.guild.get_role(admin_roles["staff"])
        embed = discord.Embed(
            title=server_info["name"],
            description=f"**- Website -**\n{server_info['website']}\n\n \
							**- Owner -**\n{interaction.guild.owner}\n\n \
							**- Email -**\n{server_info['email']}\n\n \
							**- Invite Link -**\n{server_info['invite']}\n\n \
							**- Leave a reveiw -**\n{server_info['review']}\n\n \
							**- Questions? -**\nMake a ticket using /ticket, or send us an email.",
            color=discord.Color.yellow(),
        )
        embed.set_thumbnail(url=server_info["logo"])
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Running code", row=0, style=discord.ButtonStyle.success)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message(
            """To run python code in the chat, type:\n\n/run\n\`\`\`py\nx = 'hello world'\nprint(x) \`\`\`"""
        )

    @discord.ui.button(label="Code Blocks", row=0, style=discord.ButtonStyle.success)
    async def fourth_button_callback(self, button, interaction):
        await interaction.response.send_message(
            """To format your python code like this: \n```py x = 'Hello World!' ``` Type this: \`\`\`py Your code here \`\`\`"""
        )


class helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Ask Zorak for help.")
    async def help(self, ctx):
        await ctx.respond("What do you want, human?", view=helpButtons(timeout=120))


def setup(bot):
    bot.add_cog(helper(bot))
