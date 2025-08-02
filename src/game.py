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
        self.discard_pile.append(self.deck.pop())
    
    def play_card(self, card: Card):
        if card not in self.players[self.current_player_index].hand:
            raise ValueError(f"{card.color} {card.value} is not in {self.players[self.current_player_index].name}'s hand.")
        if card.color != self.discard_pile[-1].color and card.value != self.discard_pile[-1].value:
            raise ValueError(f"{card.color} {card.value} cannot be played on top of {self.discard_pile[-1].color} {self.discard_pile[-1].value}.")
        self.discard_pile.append(card)
        self.players[self.current_player_index].hand.remove(card)
        self.current_player_index =  (self.current_player_index + 1) % len(self.players)
        return f"{self.players[self.current_player_index].name} played {card.color} {card.value}. {self.players[self.current_player_index].name}'s turn next."

    def check_winner(self) -> Optional[str]:
        for player in self.players:
            if not player.hand:
                return f"{player.name} wins!"
        return None

if __name__ == "__main__":
    from colorama import Fore
    game = UnoGame([Player(name="Alice"), Player(name="Bob")])
    game.deal_cards()
    print("Game started with players:")
    while game.check_winner() is None:
        print(f"\n================== {game.players[game.current_player_index].name}'s turn ==================")
        for player in game.players:
            print(f"{player.name} has {len(player.hand)} cards.")
        print(f"Top card on discard pile: Card({game.discard_pile[-1].color}, {game.discard_pile[-1].value})")
        print("Current hand:")
        for card in game.players[game.current_player_index].hand:
            print(f"\t- Card({card.color}, {card.value})")
        while True:
            try:
                index = input(f"{game.players[game.current_player_index].name}, press Card index to play a card (0 to {len(game.players[game.current_player_index].hand) - 1}): ")
                card_to_play = game.players[game.current_player_index].hand[int(index)]  # For simplicity, play the first card
                print(Fore.YELLOW + f"Attempting to play: Card({card_to_play.color}, {card_to_play.value})" + Fore.RESET)
                print(Fore.GREEN + game.play_card(card_to_play) + Fore.RESET)
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Fore.RESET)

