"""
Admin command for kicking a user.
"""
import logging
import discord
from discord.ext import commands
from utilities.cog_helpers._embeds import embed_cant_do_that  # pylint: disable=E0401


logger = logging.getLogger(__name__)


class AdminKick(commands.Cog):
    """
    Command to kick a user. Takes in a name, and a reason.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Kick a user.")
    @commands.has_permissions(kick_members=True)
    @commands.has_role("Staff")
    async def kick_member(self, ctx, target: discord.Member, reason):
        """
        Take in a user mention, and a string reason.
        """
        # Cant kick bots or admins.
        if not target.bot:
            if not target.guild_permissions.administrator:

                # Message the user, informing them of their fate
                await target.send(f'## You were kicked by {ctx.author.name}.\n'
                                  f'**Reason:** {reason}\n'
                                  '\nIf you wish to appeal this kick,'
                                  ' contact PracticalPythonStaff@gmail.com')
                # Then we do the kick
                await target.kick(reason=f"{ctx.author.name} - {reason}")
                logger.info("{%s} kicked {%s}. Reason: {%s}"
                            , ctx.author.name
                            , target.name
                            , reason)
                # Then we publicly announce what happened.
                await ctx.respond(
                    embed=embed_cant_do_that(
                        f"**{ctx.author.name}** kicked **{target.name}**"
                        f"\n**Reason:** {reason}")
                )

            else:
                await ctx.respond(
                    embed=embed_cant_do_that("You can't kick an Admin.")
                    , ephemeral=True)
        else:
            await ctx.respond(
                embed=embed_cant_do_that("You cant kick a bot.")
                , ephemeral=True)


def setup(bot):
    """
    required.
    """
    bot.add_cog(AdminKick(bot))
