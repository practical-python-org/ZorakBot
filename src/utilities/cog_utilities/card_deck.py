import random


class Card:
    def __init__(self, suit, value) -> None:
        self.suit = suit
        self.value = value

    def __str__(self) -> None:
        print(f"{self.value} of {self.suit}")


class Deck:
    NAME_MAPPINGS = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

    def __init__(self) -> None:
        self.cards = []
        self.build()

    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range(1, 14):
                if v in self.NAME_MAPPINGS:
                    self.cards.append(Card(s, self.NAME_MAPPINGS[v]))
                else:
                    self.cards.append(Card(s, v))

    def draw_card(self):
        return self.cards.pop()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def print_deck(self):
        for c in self.cards:
            c.print_value()
