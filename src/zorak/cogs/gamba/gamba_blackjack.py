"""
Blackjack. 
"""
import json
import logging
import random
from random import choice
import discord
from discord.ext import commands
from zorak.utilities.cog_utilities.card_deck import Deck

logger = logging.getLogger(__name__)

# read cards.json
with open("src/zorak/cogs/gamba/cards.json") as f:
    cards = json.load(f)
    
# read cards_mapping_lowercase.json
with open("src/zorak/cogs/gamba/cards_mapping_lowercase.json") as f:
    cards_mapping_lowercase = json.load(f)

class MessageFormatter:
    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
       
    def welcome_message(self):
        return f"Welcome to Blackjack. Dealer stands at 17."
    
    def player_hand_message(self):
        message = "# Your hand: "
        for card in self.player.hand:
            card_value = str(card.value)[0] if not str(card.value).isdigit() else str(card.value)
            card_key = f"{card_value}{str(card.suit)}".lower()
            emoji_id = cards[cards_mapping_lowercase[card_key]]
            message += f"<:{card_key}:{emoji_id}>"
        
        # message = message[:-4]
        message += f"\nYou're on {str(self.player.score)}."
        return message
    
    def dealer_hand_message(self):
        message = "# Dealer's hand: "
        for card in self.dealer.hand:
            card_value = str(card.value)[0] if not str(card.value).isdigit() else str(card.value)
            card_key = f"{card_value}{str(card.suit)}".lower()
            emoji_id = cards[cards_mapping_lowercase[card_key]]
            message += f"<:{card_key}:{emoji_id}>"
            
        #message = message[:-4]
        message += f"\nDealer is on {str(self.dealer.score)}."
        return message

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
            elif card.value in ["Jack", "Queen", "King"]:
                score += 10
        while score > 21 and num_aces > 0:
            score -= 10
            num_aces -= 1
        return score
    
class BlackjackGame:
    def __init__(self, player_name, player_bet, user_id, bot):
        self.player = Player(player_name)
        self.dealer = Player("Dealer")
        self.deck = Deck()
        self.deck.shuffle()
        self.player_bet = player_bet
        self.user_id = user_id
        self.bot = bot

    def deal(self):
        self.player.draw_card(self.deck)
        self.dealer.draw_card(self.deck)
        self.player.draw_card(self.deck)
        self.dealer.draw_card(self.deck)

    def player_hit(self):
        self.player.draw_card(self.deck)

    def dealer_hit(self):
        self.dealer.draw_card(self.deck)

class BlackjackView(discord.ui.View):
    def __init__(self, *, game, timeout=300):
        super().__init__(timeout=timeout)
        self.game = game

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.game.player_hit()
        if self.game.player.score > 21:
            for child in self.children:
                child.disabled = True
                card = self.game.player.hand[-1]
                self.game.bot.db_client.add_points_to_user(self.game.user_id, -self.game.player_bet)
                await interaction.response.edit_message( # @TODO - check if this is taking away points
                    content=f"You drew a {str(card.value)} of {str(card.suit)} and busted with {str(self.game.player.score)}!\nYou lost {str(self.game.player_bet)} points.",
                    view=self,
                )    
            return
        card = self.game.player.hand[-1]

        # use formatter to get the message
        await interaction.response.edit_message(
            content=f"You drew a {str(card.value)} of {str(card.suit)}.\n{MessageFormatter(self.game.player, self.game.dealer).player_hand_message()}\n{MessageFormatter(self.game.player, self.game.dealer).dealer_hand_message()}", view=self
        )
    
    # disable button on bust
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        
        if self.game.player.score > 21:
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(
                content=f"You're bust! You can't stand.",
                view=self
            )
            return
        
        for child in self.children:
            child.disabled = True

        while self.game.dealer.score < 17:
            self.game.dealer_hit()
        if self.game.dealer.score > 21:
            await interaction.response.edit_message(
                content=f"Dealer busted with {str(self.game.dealer.score)}. You win {str(self.game.player_bet)} points!", view=self
            )
            self.game.bot.db_client.add_points_to_user(self.game.user_id, self.game.player_bet)
        elif self.game.dealer.score > self.game.player.score:
            await interaction.response.edit_message(
                content=f"Dealer wins with {str(self.game.dealer.score)} against your {str(self.game.player.score)}. You lose {str(self.game.player_bet)} points.",
                view=self,
            )
            self.game.bot.db_client.add_points_to_user(self.game.user_id, -self.game.player_bet)
        elif self.game.dealer.score < self.game.player.score:
            await interaction.response.edit_message(
                content=f"You win with {str(self.game.player.score)}!\nDealer got {str(self.game.dealer.score)}. You win {str(self.game.player_bet)}", view=self
            )
            self.game.bot.db_client.add_points_to_user(self.game.user_id, self.game.player_bet)
        else: 
            await interaction.response.edit_message(
                content=f"It's a tie! You both got {str(self.game.player.score)}.", view=self
            )

class Blackjack(commands.Cog):
    """
    # Blackjack
    """

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        
        # !blackjack 1000
        
        if message.content.startswith('!blackjack'):
            
            parsed = message.content.split()
            
            try:
                points = int(parsed[1])
            except ValueError:
                await message.channel.send("You need to bet full points! example: !blackjack 1000")
                return
            
            if points < 0:
                await message.channel.send("You betting negative points? You are a madman!")
                return
            
            if points == 0:
                await message.channel.send("You betting zero points? You are a coward!")
                return
            
            if points > 0:
                if points > self.bot.db_client.get_user_points(message.author.id):
                    await message.channel.send("You don't have enough points!")
                    return
            
            id = message.author.id
            
            game = BlackjackGame(message.author.name, points, id, self.bot)
            game.deal()
            view = BlackjackView(game=game)
            
            formatter = MessageFormatter(game.player, game.dealer)
            
            welcome_message = formatter.welcome_message()
            player_hand_message = formatter.player_hand_message()
            dealer_hand_message = formatter.dealer_hand_message()
            
            await message.channel.send(
                f"{welcome_message}\n{player_hand_message}\n{dealer_hand_message}", view=view)

def setup(bot):
    """
    Required.
    """
    bot.add_cog(Blackjack(bot))