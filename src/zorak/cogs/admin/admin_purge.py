"""
Admin command to remove messages in bulk.
"""
from discord.ext import commands


class AdminPurge(commands.Cog):
    """
    We are limited to 100 messages per command by Discord API
    TODO: This command should be hidden from non-staff users.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Removes up to 100 messages from channel.")
    @commands.has_permissions(manage_messages=True)
    @commands.has_role("Staff")
    async def purge_messages(self, ctx, number_messages):
        """
        We currently have permissions on this command set,
        which throws an error when the user does not have the correct perms.
        We handle this with an error_handler block
        """

        # removes the need for a response
        await ctx.defer()
        logs_channel = await self.bot.fetch_channel(self.bot.settings.logging["mod_log"])  # Welcome channel

        # Do the purge
        await ctx.channel.purge(limit=int(number_messages))
        # Log the purge
        await logs_channel.send(f"{number_messages} messages purged" f" from {ctx.channel.mention}" f" by {ctx.author.mention}.")

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        Handles errors for this cog
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(
                f"Sorry, {ctx.author.name}, you dont have the " f"correct permissions to use this command!",
                reference=ctx.message,
            )

        if isinstance(error, commands.MissingRole):
            await ctx.channel.send(
                f"Sorry, {ctx.author.name}, you must be a" f" memeber of Staff to use this command!",
                reference=ctx.message,
            )


def setup(bot):
    """
    required by all cogs.
    """
    bot.add_cog(AdminPurge(bot))
