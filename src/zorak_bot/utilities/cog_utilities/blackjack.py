# I've moved this here for now so it doesnt get loaded on the bot as it's not quite finished.
# You can ignore this for now, I'll move it in when it's done and put another PR in.

import discord
from discord.ext import commands

from zorak_bot.utilities.cog_utilities.card_deck import Deck


class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def blackjack(ctx):
        game = BlackjackGame(ctx.author.name)
        game.deal()
        view = BlackjackView(game=game)
        await ctx.send("Welcome to Blackjack. Dealer stands at 17.", view=view)


class BlackjackView(discord.ui.View):
    def __init__(self, *, game, timeout=300):
        super().__init__(timeout=timeout)
        self.game = game

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.game.player_hit()
        if self.game.player.score > 21:
            for child in self.children:
                child.disabled = True
                await interaction.response.edit_message(
                    f"You drew a {str(self.game.player.hand[-1])} and busted with {str(self.game.player.score)}!", view=self
                )
        await interaction.response.edit_message(
            f"You drew a {str(self.game.player.hand[-1])}. You're on {str(self.game.player.score)}. Hit or Stand?", view=self
        )

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True

        while self.game.dealer.score < 17:
            self.game.dealer_hit()
        if self.game.dealer.score > 21:
            await interaction.response.edit_message(f"Dealer busted. You win!", view=self)
        elif self.game.dealer.score > self.game.player.score:
            await interaction.response.edit_message(
                f"Dealer wins with {str(self.game.dealer.score)} against your {str(self.game.player.score)}.", view=self
            )
        elif self.game.dealer.score < self.game.player.score:
            await interaction.response.edit_message(f"You win with {str(self.game.player.score)}!", view=self)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def draw_card(self, deck):
        self.hand.append(deck.draw_card())
        self.score = self.calculate_score()

    def calculate_score(self):
        score = 0
        num_aces = 0
        for card in self.hand:
            if card.value == "Ace":
                num_aces += 1
                score += 11
            elif isinstance(card.value, int) and card.value > 1:
                score += card.value
        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1
        return score


class BlackjackGame:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.dealer = Player("Dealer")
        self.deck = Deck()
        self.deck.shuffle()

    def deal(self):
        self.player.draw_card(self.deck)
        self.dealer.draw_card(self.deck)
        self.player.draw_card(self.deck)
        self.dealer.draw_card(self.deck)

    def player_hit(self):
        self.player.draw_card(self.deck)

    def dealer_hit(self):
        self.dealer.draw_card(self.deck)
