import discord
from discord.ext import commands

# Here I'm going to use the new MongoDB database to create some infrastructure to allow users to accumalate
# points for actions taken in the server. This will be used to create a leaderboard and to reward users
# for their activity in the server.


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
        if message.author.bot:
            return
        self.bot.db_client.remove_points_from_user(message.author.id, 1)

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    async def backup_db(self, ctx, save_file_name: discord.Option(str)):
        """Backup the MongoDB instance."""
        self.bot.db_client.backup_db(save_file_name)
        await ctx.send("Database backed up.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    def add_all_members_to_db(self, ctx):
        """Add all members to the database."""
        self.bot.db_client.create_table_from_members(ctx.guild.members)
        ctx.send("All members added to database.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    def add_points_to_user(self, ctx, mention: discord.Option(str), points: discord.Option(int)):
        """Add points to a user."""
        user = self.bot.get_user(mention.split("@")[1].split(">")[0])
        self.bot.db_client.add_points_to_user(user.id, points)
        ctx.send(f"{points} points added to {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    def add_points_to_all_users(self, ctx, points: discord.Option(int)):
        """Add points to all users."""
        self.bot.db_client.add_points_to_all_users(points)
        ctx.send(f"{points} points added to all users.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    def remove_points_from_user(self, ctx, mention: discord.Option(str), points: discord.Option(int)):
        """Remove points from a user."""
        user = self.bot.get_user(mention.split("@")[1].split(">")[0])
        self.bot.db_client.remove_points_from_user(user.id, points)
        ctx.send(f"{points} points removed from {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    def remove_points_from_all_users(self, ctx, points: discord.Option(int)):
        """Remove points from all users."""
        self.bot.db_client.remove_points_from_all_users(points)
        ctx.send(f"{points} points removed from all users.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    def reset_points_for_user(self, ctx, mention: discord.Option(str)):
        """Reset points for a user."""
        user = self.bot.get_user(mention.split("@")[1].split(">")[0])
        self.bot.db_client.set_user_points(user.id, 0)
        ctx.send(f"Points reset for {mention}.")

    @commands.slash_command()
    @commands.has_any_role("Staff", "Owner", "Project Manager")
    def reset_points_for_all_users(self, ctx):
        """Reset points for all users."""
        self.bot.db_client.set_all_user_points(0)
        ctx.send("Points reset for all users.")

    @commands.slash_command()
    def my_points(self, ctx):
        """Get your points."""
        points = self.bot.db_client.get_user_points(ctx.author.id)
        ctx.send(f"You have {points} points.")

    @commands.slash_command()
    def get_points_for_user(self, ctx, mention: discord.Option(str)):
        """Get points for a user."""
        user = self.bot.get_user(mention.split("@")[1].split(">")[0])
        points = self.bot.db_client.get_user_points(user.id)
        ctx.send(f"{mention} has {points} points.")

    def get_user_points(self, user_id: str):
        """Get a users points."""
        return self.bot.db_client.get_user_points(user_id)
