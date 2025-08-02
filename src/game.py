import random
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class CardColor(Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"
    BLACK = "Black"

class CardValue(Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    SKIP = "Skip"
    REVERSE = "Reverse"
    DRAW_TWO = "Draw Two"
    WILD = "Wild"
    WILD_DRAW_FOUR = "Wild Draw Four"

class Card(BaseModel):
    color: str
    value: str

class Player(BaseModel):
    name: str
    hand: Optional[list[Card]] = []

class UnoGame:
    def __init__(self, players: list[Player]):
        self.players = players
        self.current_player_index = 0
        self.deck = self.create_deck()
        self.discard_pile = []
    
    @staticmethod
    def create_deck() -> list[Card]:
        deck = []
        for color in CardColor:
            if color == CardColor.BLACK:
                deck.extend([Card(color=color.value, value=CardValue.WILD.value) for _ in range(4)])
                deck.extend([Card(color=color.value, value=CardValue.WILD_DRAW_FOUR.value) for _ in range(4)])
            else:
                deck.append(Card(color=color.value, value=CardValue.ZERO.value))
                for value in CardValue:
                    if value not in [CardValue.ZERO, CardValue.WILD, CardValue.WILD_DRAW_FOUR]:
                        deck.extend([Card(color=color.value, value=value.value) for _ in range(2)])
        return deck

    def deal_cards(self):
        random.shuffle(self.deck)
        for player in self.players:
            player.hand = [self.deck.pop() for _ in range(7)]
    
    def play_card(self, card):
        # Logic for playing a card
        pass

    def next_player(self):
        # Logic to switch to the next player
        pass

if __name__ == "__main__":
    game = UnoGame([Player(name="Alice"), Player(name="Bob")])
    print(game.players)
    game.deal_cards()
    print(game.players)