"""
Creates an embed for use in rescources, rules... whatever.
TODO: This dude here is broken as hell. fix it.
"""
import discord
from discord.ext import commands


class AdminEmbed(commands.Cog):
    """
    An embed command that embeds text into a nice format.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, title, content):
        """
        Handles text that is bigger than the standard size for an embed
        by splitting it into chunks and adding them all together.
        """
        text = ctx.message.content.split("\n")
        embed = discord.Embed(title=title)
        # TODO: This here is probably what's broken.
        content = [
            embed.add_field(name=" ----- ", value=item, inline=False) for item in text
        ]  # Nice
        embed.add_field(name="Content", value=content)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    async def cog_command_error(
            self, ctx: commands.Context, error: commands.CommandError
    ):
        """
        Error handling for the entire Admin Cog
        """

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"Sorry, {ctx.author.name}, you dont have permission to use this command!",
                reference=ctx.message,
            )
        else:
            raise error


def setup(bot):
    """
    Required.
    """
    bot.add_cog(AdminEmbed(bot))
