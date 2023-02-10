import discord
from discord.ext import commands

from ._settings import log_channel


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        self.bot.db_client.add_member_to_table(member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        self.bot.db_client.remove_member_from_table(member.id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        self.bot.db_client.add_points_to_user(message.author.id, 1)

    # Small abuse stopper. If a user deletes a message, they lose a point.
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(
            f"1 Point removed from {message.author} for deleting a message."
        )
        self.bot.db_client.remove_points_from_user(message.author.id, 1)

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
        self, ctx, mention: discord.Option(str), points: discord.Option(int)
    ):
        """Add points to a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        self.bot.db_client.add_points_to_user(user.id, points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(f"{points} point{('s','')[abs(points)==1]} added to {mention} by {ctx.author}.")
        await ctx.respond(f"{points} point{('s','')[abs(points)==1]} added to {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def add_points_to_all_users(self, ctx, points: discord.Option(int)):
        """Add points to all users."""
        self.bot.db_client.add_points_to_all_users(points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(f"{points} point{('s','')[abs(points)==1]} added to all users by {ctx.author}.")
        await ctx.respond(f"{points} point{('s','')[abs(points)==1]} added to all users.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def remove_points_from_user(
        self, ctx, mention: discord.Option(str), points: discord.Option(int)
    ):
        """Remove points from a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        self.bot.db_client.remove_points_from_user(user.id, points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(f"{points} point{('s','')[abs(points)==1]} removed from {mention} by {ctx.author}.")
        await ctx.respond(f"{points} point{('s','')[abs(points)==1]} removed from {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def remove_points_from_all_users(self, ctx, points: discord.Option(int)):
        """Remove points from all users."""
        self.bot.db_client.remove_points_from_all_users(points)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(f"{points} point{('s','')[abs(points)==1]} removed from all users by {ctx.author}.")
        await ctx.respond(f"{points} point{('s','')[abs(points)==1]} removed from all users.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def reset_points_for_user(self, ctx, mention: discord.Option(str)):
        """Reset points for a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        self.bot.db_client.set_user_points(user.id, 0)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(f"Points reset for {mention} by {ctx.author}.")
        await ctx.respond(f"Points reset for {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def reset_points_for_all_users(self, ctx):
        """Reset points for all users."""
        self.bot.db_client.set_all_user_points(0)
        mod_log = await self.bot.fetch_channel(log_channel["mod_log"])
        await mod_log.send(f"Points reset for all users by {ctx.author}.")
        await ctx.respond("Points reset for all users.")

    @commands.slash_command()
    async def my_points(self, ctx):
        """Get your points."""
        points = self.bot.db_client.get_user_points(ctx.author.id)
        await ctx.respond(f"You have {points} point{('s','')[abs(points)==1]}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def get_points_for_user(self, ctx, mention: discord.Option(str)):
        """Get points for a user."""
        user = self.bot.get_user(int(mention.split("@")[1].split(">")[0]))
        points = self.bot.db_client.get_user_points(user.id)
        await ctx.respond(f"{mention} has {points} point{('s','')[abs(points)==1]}.")


def setup(bot):
    bot.add_cog(Points(bot))
