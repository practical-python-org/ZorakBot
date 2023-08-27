"""
This is a retired command that issued the daily challenge for 50 Days of code
"""
import discord
from discord.ext import commands


class Challenges(commands.Cog):
    """
    Oh wow this is bad code.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def challenge(self, ctx, day):
        """
        This checks for admin, then reads a .txt file, replaces some odd content,
        and then sends each day to the embed. Can't believe this worked lol.
        """
        isadmin = ctx.author
        if "Staff" in [role.name for role in isadmin.roles]:
            with open(
                "50-Days-of-Python.txt", encoding="utf-8"
            ) as file:  # TODO verify this isn't broken
                file = file.read()
                file = file.replace("Day ", "$$$$$Day ")
                all_days = file.split("$$$$$")
                for current_day in all_days:
                    if current_day.startswith(f"Day {day}:"):

                        # Make the embed
                        embed = discord.Embed(
                            title="Practical Python's 50 days of code",
                            description="Please place only **finished answers** "
                                        "in the thread. Any challenge related "
                                        "discussions should happen in the help channels.",
                            color=discord.Color.dark_green(),
                        )
                        embed.set_thumbnail(
                            url="https://raw.githubusercontent.com/Xarlos89/"
                                "PracticalPython/main/logo.png"
                        )
                        embed.add_field(
                            name=f"Challenge #{day}:", value=current_day, inline=True
                        )
                        embed.set_footer(
                            text="Brought to you by: Benjamin Bennett Alexander's "
                                 "50 Days of Python "
                        )
                        await ctx.respond(embed=embed)

                        # TODO: this was never used
                        # Open the thread
                        # channel = await self.bot.fetch_channel(
                        #     1045104938071633994
                        # )  # CHALLENGES channel
                        thread = await ctx.channel.create_thread(
                            name=f"Challenge #{day}",
                            type=discord.ChannelType.public_thread,
                        )

                        help1 = await self.bot.fetch_channel(903542455675260928)
                        help2 = await self.bot.fetch_channel(903542494409674803)
                        await thread.send(
                            f"Please place only **finished answers** for "
                            f"**Day {day}** in this thread.\nAny challenge "
                            f"related discussions should happen in {help1.mention}"
                            f" or {help2.mention}."
                        )
        else:
            await ctx.respond(
                "Only a member of the <@&960232134356901959> can launch a challenge.",
                ephemeral=True,
            )


def setup(bot):
    """
    required
    """
    bot.add_cog(Challenges(bot))
