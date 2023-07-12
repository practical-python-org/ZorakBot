"""
logs when a username is changed.
"""
from discord.ext import commands
from utilities.cog_helpers._embeds\
    import embed_name_change, embed_verified_success  # pylint: disable=E0401
from cogs._settings import log_channel  # pylint: disable=E0401


class LoggingNameChanges(commands.Cog):
    """
    Simple listener to on_member_update
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Just checking if the name before is != to the name after.
        """
        if before.nick is None:
            username_before = before
        else:
            username_before = before.nick

        if after.nick is None:
            username_after = after
        else:
            username_after = after.nick

        if before.nick != after.nick and before.nick is not None:
            embed = embed_name_change(before, after, username_before, username_after)

            logs_channel = await self.bot.fetch_channel(log_channel['mod_log'])
            await logs_channel.send(f'{username_after.mention}', embed=embed)

        # Verification success logging
        # TODO: Find a way to pull this into it's own cog.
        elif "Needs Approval" in [
            role.name for role in before.roles
        ] and "Needs Approval" not in [
            role.name for role in after.roles
        ]:

            logs_channel = await self.bot.fetch_channel(log_channel["join_log"])  # user join logs
            embed = embed_verified_success(username_after, after.guild.member_count)

            await logs_channel.send(f"{username_after.mention}", embed=embed)


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingNameChanges(bot))
