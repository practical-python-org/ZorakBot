"""
The point handler for the whole server.
"""
import discord
from discord.ext import commands
from cogs._settings import log_channel, server_info, admin_roles  # pylint: disable=E0401

from utilities.cog_helpers._embeds import embed_leaderboard



class Points(commands.Cog):
    """
     Handles automatic points based on activity.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):  # pylint: disable=E1101
        """When a member joins, add them to the DB."""
        self.bot.db_client.add_user_to_table(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):  # pylint: disable=E1101
        """When a member leaves, remove them from the DB."""
        self.bot.db_client.remove_user_from_table(member)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """When a member sends a message, give them 1 point."""
        if message.author.bot:
            return
        self.bot.db_client.add_points_to_user(message.author.id, 1)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """When a member deletes a message, remove a point."""
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"1 Point removed from {message.author} for deleting a message."
        )
        self.bot.db_client.remove_points_from_user(message.author.id, 1)

    # TODO: Fix the backup command.
    # @commands.slash_command()
    # @commands.has_any_role("Staff", "Owner", "Project Manager")
    # async def backup_db(self, ctx):
    #     """Backup the MongoDB instance."""
    #     self.bot.db_client.backup_db()
    #     await ctx.respond("Database backed up.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def add_all_members_to_db(self, ctx):
        """Add all members to the database."""
        self.bot.db_client.create_table_from_members(ctx.guild.members)
        await ctx.respond("All members added to database.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def add_points_to_user(
            self, ctx, mention: discord.Option(str), points: discord.Option(int)  # pylint: disable=E1101
    ):
        """Add points to a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        self.bot.db_client.add_points_to_user(user.id, points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"{points} point{('s', '')[abs(points) == 1]} added to {mention} by {ctx.author}.")
        await ctx.respond(
            f"{points} point{('s', '')[abs(points) == 1]} added to {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def add_points_to_all_users(self, ctx, points: discord.Option(int)):  # pylint: disable=E1101
        """Add points to all users."""
        self.bot.db_client.add_points_to_all_users(points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"{points} point{('s', '')[abs(points) == 1]} added to all users by {ctx.author}.")
        await ctx.respond(
            f"{points} point{('s', '')[abs(points) == 1]} added to all users.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def remove_points_from_user(
            self, ctx, mention: discord.Option(str), points: discord.Option(int)  # pylint: disable=E1101
    ):
        """Remove points from a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        self.bot.db_client.remove_points_from_user(user.id, points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"{points} point{('s', '')[abs(points) == 1]} removed from {mention} by {ctx.author}.")
        await ctx.respond(
            f"{points} point{('s', '')[abs(points) == 1]} removed from {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def remove_points_from_all_users(self, ctx, points: discord.Option(int)):  # pylint: disable=E1101
        """Remove points from all users."""
        self.bot.db_client.remove_points_from_all_users(points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"{points} point{('s', '')[abs(points) == 1]} removed from all users by {ctx.author}.")
        await ctx.respond(
            f"{points} point{('s', '')[abs(points) == 1]} removed from all users.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def reset_points_for_user(self, ctx, mention: discord.Option(str)):  # pylint: disable=E1101
        """Reset points for a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        self.bot.db_client.set_user_points(user.id, 0)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"Points reset for {mention} by {ctx.author}.")
        await ctx.respond(
            f"Points reset for {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def reset_points_for_all_users(self, ctx):
        """Reset points for all users."""
        self.bot.db_client.set_all_user_points(0)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"Points reset for all users by {ctx.author}.")
        await ctx.respond(
            "Points reset for all users.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def get_points_for_user(self, ctx, mention: discord.Option(str)):  # pylint: disable=E1101
        """Get points for a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        points = self.bot.db_client.get_user_points(user.id)
        await ctx.respond(f"{mention} has {points} point{('s', '')[abs(points) == 1]}.")

    @commands.slash_command()
    async def leaderboard(self, ctx):
        """Get your points."""

        def is_staff(member_obj):
            """ Tells us if the 'member_obj' has an admin role. """
            for role in admin_roles:
                if admin_roles[role] in [y.id for y in member_obj.roles]:
                    return True
            return False

        top10_no_staff = []
        points = self.bot.db_client.get_top_10()
        guild = self.bot.get_guild(server_info['id'])
        for person in points:
            member = guild.get_member(person['UserID'])
            if not is_staff(member):
                top10_no_staff.append((member, person['Points']))

        embed = embed_leaderboard(top10_no_staff)
        await ctx.respond(embed=embed)



def setup(bot):
    """required"""
    bot.add_cog(Points(bot))
