import discord
from discord.ext import commands
from datetime import datetime
from ._settings import log_channel


class logging_nameChanges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick is None:
            username_before = before
        else:
            username_before = before.nick

        if after.nick is None:
            username_after = after
        else:
            username_after = after.nick

        if before.nick != after.nick and before.nick is not None:
            embed = discord.Embed(
                title="<:grey_exclamation:1044305627201142880> Name Change",
                description=f"Changed by: {before}.",
                color=discord.Color.dark_grey(),
                timestamp=datetime.utcnow(),
            )
            embed.set_thumbnail(url=after.avatar)
            embed.add_field(name="Before", value=username_before, inline=True)
            embed.add_field(name="After", value=username_after, inline=True)

            logs_channel = await self.bot.fetch_channel(
                log_channel["user_log"]
            )  # ADMIN user log
            await logs_channel.send(f"{username_after.mention}", embed=embed)

        # Verification success logging
        elif "Needs Approval" in [
            role.name for role in before.roles
        ] and "Needs Approval" not in [role.name for role in after.roles]:
            logs_channel = await self.bot.fetch_channel(
                log_channel["join_log"]
            )  # user join logs
            embed = discord.Embed(
                title="",
                description=f"{username_after}, human number {after.guild.member_count} has joined.",
                color=discord.Color.dark_green(),
            )
            await logs_channel.send(f"{username_after.mention}", embed=embed)


def setup(bot):
    bot.add_cog(logging_nameChanges(bot))
