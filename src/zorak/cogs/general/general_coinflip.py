"""
Simple coinflip command.
"""
import logging
from random import choice
import discord
from discord.commands import option
from discord.ext import commands

logger = logging.getLogger(__name__)


class GambaCoinflip(commands.Cog):
    """
    # GAMBA?!
    """

    def __init__(self, bot):
        self.bot = bot
        self.coin_options = ["Heads", "Tails"]
        self.bet_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    async def get_sides(self, ctx: discord.AutocompleteContext):
        """Helper function for the coin sides arg"""
        return [item for item in self.coin_options if item.startswith(ctx.value.lower())]

    async def get_bets(self, ctx: discord.AutocompleteContext):
        """Helper function for the bet amount arg"""
        return [num for num in self.bet_options if str(num).startswith(str(ctx.value))]

    @commands.slash_command(name="coinflip")
    @option("side", description="Heads or Tails?", autocomplete=get_sides)
    @option("bet", description="Bet amount", autocomplete=get_bets)
    async def coinflip(self, ctx: discord.ApplicationContext, side: str, bet_amount: int):
        """Flips a coin, adds or removes points from the user based on their bet."""

        # Get Off Topic channel for response
        channel = next((c for c in ctx.guild.channels if c.name == "📁-off-topic"), None)
        ping = ctx.author.mention

        wallet = self.bot.db_client.get_user_points(int(ctx.user.id))

        if wallet is None:
            # User is not yet added to the DB
            self.bot.db_client.add_user_to_table(ctx.author)
            await channel.send(
                f"{ping}\nYou have no points yet.\n"
                "You can get points by chatting in the server,"
                " or by doing things that make mods happy.")
            return

        if bet_amount < 0:
            await channel.send(f"{ping}\nYou betting negative points? You are a madman!")
            return

        if bet_amount == 0:
            await channel.send(f"{ping}\nYou betting zero points? You are a coward!")
            return

        if wallet < bet_amount:
            # User is trying to be a sly little fox
            await channel.send(
                f"{ping}\nYou can't bet **{bet_amount:,}** points"
                f", because you only have **{wallet:,}**")
            return

        if wallet >= bet_amount:
            # Do you want to play a game?
            coin = choice(self.coin_options)
            name = ctx.author.name if ctx.author.nick is None else ctx.author.nick

            if coin == side:
                status = "won"
                bet_result = bet_amount
            else:
                status = "lost"
                bet_result = -bet_amount

            await channel.send(
                f"{ping} flipped a coin and chose **{side}**\n"
                f"The coin landed on **{coin}**!\n"
                f"You {status} **{bet_amount:,} points**!\n"
                f"You now have **{(wallet + bet_result):,} points!**")
            self.bot.db_client.add_points_to_user(ctx.author.id, bet_result)
            return


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GambaCoinflip(bot))
