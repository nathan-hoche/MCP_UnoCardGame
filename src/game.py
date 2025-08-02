import random
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from colorama import Fore

class CardColor(Enum):
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    BLACK = "BLACK"

class ColorEnum(Enum):
    RED = Fore.RED
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    YELLOW = Fore.YELLOW
    BLACK = Fore.BLACK

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
        self.discard_pile.append(self.deck.pop())
    
    def play_card(self, card: Card):
        if card not in self.players[self.current_player_index].hand:
            raise ValueError(f"{card.color} {card.value} is not in {self.players[self.current_player_index].name}'s hand.")
        if card.color != self.discard_pile[-1].color and card.value != self.discard_pile[-1].value:
            raise ValueError(f"{card.color} {card.value} cannot be played on top of {self.discard_pile[-1].color} {self.discard_pile[-1].value}.")
        self.discard_pile.append(card)
        self.players[self.current_player_index].hand.remove(card)
        played = f"{self.players[self.current_player_index].name} played Card({ColorEnum[card.color].value}{card.value}{Fore.RESET})."
        self.current_player_index =  (self.current_player_index + 1) % len(self.players)
        return played + f" {self.players[self.current_player_index].name}'s turn next."

    def draw_card(self):
        if not self.deck:
            raise ValueError("The deck is empty, cannot draw a card.")
        drawn_card = self.deck.pop()
        self.players[self.current_player_index].hand.append(drawn_card)
        return f"{self.players[self.current_player_index].name} drew a card: Card({ColorEnum[drawn_card.color].value}{drawn_card.value}{Fore.RESET})"

    def check_winner(self) -> Optional[str]:
        for player in self.players:
            if not player.hand:
                return f"{player.name} wins!"
        return None

if __name__ == "__main__":
    game = UnoGame([Player(name="Alice"), Player(name="Bob")])
    game.deal_cards()
    print("Game started with players:")
    while game.check_winner() is None:
        print(f"\n================== {game.players[game.current_player_index].name}'s turn ==================")
        for player in game.players:
            print(f"{player.name} has {len(player.hand)} cards.")
        print(f"Top card on discard pile: Card({ColorEnum[game.discard_pile[-1].color].value}{game.discard_pile[-1].value}{Fore.RESET})")
        print("Current hand:")
        for card in game.players[game.current_player_index].hand:
            print(f"\t- Card({ColorEnum[card.color].value}{card.value}{Fore.RESET})")
        while True:
            try:
                index = input(f"{game.players[game.current_player_index].name}, press Card index to play a card (0 to {len(game.players[game.current_player_index].hand) - 1}) or draw: ")
                if index.lower() == 'draw':
                    print(game.draw_card())
                    continue
                card_to_play = game.players[game.current_player_index].hand[int(index)]  # For simplicity, play the first card
                print(f"Attempting to play: Card({ColorEnum[card.color].value}{card.value}{Fore.RESET})")
                print(game.play_card(card_to_play))
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Fore.RESET)

