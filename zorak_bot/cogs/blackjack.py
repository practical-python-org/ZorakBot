from zorak_bot.utilities.cog_utilities.card_deck import Deck

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

class Blackjack:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.dealer = Player("Dealer")
        self.deck = Deck()
        self.deck.shuffle()
        
    def play(self):
        # Deal initial cards
        self.player.draw_card(self.deck)
        self.player.draw_card(self.deck)
        self.dealer.draw_card(self.deck)
        self.dealer.draw_card(self.deck)
        
        # Player turn
        while self.player.decide_hit_or_stand():
            self.player.draw_card(self.deck)
            print(f"{self.player.name} draws a {self.player.hand[-1]}")
            if self.player.score > 21:
                print(f"{self.player.name} busts!")
                break
        
        # Dealer turn
        if self.player.score <= 21:
            while self.dealer.score < 17:
                self.dealer.draw_card(self.deck)
                print(f"Dealer draws a {self.dealer.hand[-1]}")
                if self.dealer.score > 21:
                    print("Dealer busts!")
                    break
                    
        # Determine winner
        if self.player.score > 21:
            print("Dealer wins!")
        elif self.dealer.score > 21:
            print(f"{self.player.name} wins!")
        elif self.player.score > self.dealer.score:
            print(f"{self.player.name} wins!")
        elif self.dealer.score > self.player.score:
            print("Dealer wins!")
        else:
            print("It's a tie!")

        