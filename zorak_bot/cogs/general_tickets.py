import discord
from discord.ext import commands
from zorak_bot.cogs._settings import mod_channel, log_channel, admin_roles
from __main__ import bot


class make_a_ticket(discord.ui.View):
    @discord.ui.button(label="Open a support Ticket", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        await interaction.response.defer()
        mod_log = await bot.fetch_channel(log_channel['mod_log'])
        support = await bot.fetch_channel(mod_channel['server_support'])
        staff = interaction.guild.get_role(admin_roles['staff'])

        ticket = await support.create_thread(name=f"[Ticket] - {interaction.user}"
                                    , message=None
                                    , auto_archive_duration=4320
                                    , type=discord.ChannelType.private_thread
                                    , reason=None)

        for person in interaction.guild.members:
            if staff in person.roles:
                await ticket.add_user(person)

        await ticket.add_user(interaction.user)
        await ticket.send(f'**{interaction.user.mention}, we have received your ticket.**')
        await ticket.send(f'To better help you, please describe your issue.')
        await mod_log.send(f'{interaction.user} created a Support ticket: <#{ticket.id}>')

        button.label = "Ticket Created!"
        button.disabled = True
        await interaction.edit_original_response(view=self)



class add_ticket_button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ticket(self, ctx):
        await ctx.respond("Do you need help, or do you have a question for the Staff?"
                          , view=make_a_ticket()
                          , ephemeral=True)


def setup(bot):
    bot.add_cog(add_ticket_button(bot))
