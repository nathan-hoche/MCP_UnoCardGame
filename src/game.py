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

    def deal_cards(self, num_cards: int = 1):
        random.shuffle(self.deck)
        for player in self.players:
            player.hand = [self.deck.pop() for _ in range(num_cards)]
        self.discard_pile.append(self.deck.pop())
    
    def play_card(self, card: Card, color_choice: Optional[str] = None) -> str:
        if card not in self.players[self.current_player_index].hand:
            raise ValueError(f"{card.color} {card.value} is not in {self.players[self.current_player_index].name}'s hand.")
        if card.color != CardColor.BLACK.value and card.color != self.discard_pile[-1].color and card.value != self.discard_pile[-1].value:
            raise ValueError(f"{card.color} {card.value} cannot be played on top of {self.discard_pile[-1].color} {self.discard_pile[-1].value}.")
        
        self.players[self.current_player_index].hand.remove(card)
        if card.color == CardColor.BLACK.value:
            if color_choice is None or color_choice not in ColorEnum.__members__:
                raise ValueError("A color must be chosen when playing a Wild card.")
            card.color = color_choice
        self.discard_pile.append(card)
        played = f"{self.players[self.current_player_index].name} played Card({ColorEnum[card.color].value}{card.value}{Fore.RESET})."
        self.card_effects(card)
        self.current_player_index =  (self.current_player_index + 1) % len(self.players)
        return played + f" {self.players[self.current_player_index].name}'s turn next."

    def card_effects(self, card: Card):
        if card.value == CardValue.DRAW_TWO.value or card.value == CardValue.WILD_DRAW_FOUR.value:
            next_player_index = (self.current_player_index + 1) % len(self.players)
            for _ in range(2 if card.value == CardValue.DRAW_TWO.value else 4):
                if not self.deck:
                    raise ValueError("The deck is empty, cannot draw a card.")
                self.players[next_player_index].hand.append(self.deck.pop())
                print(f"{self.players[next_player_index].name} drew a card: Card({ColorEnum[self.players[next_player_index].hand[-1].color].value}{self.players[next_player_index].hand[-1].value}{Fore.RESET})")
        elif card.value == CardValue.REVERSE.value:
            self.players.reverse()
            self.current_player_index = (len(self.players) - 1) - self.current_player_index
            print(f"Direction reversed! Now it's {self.players[self.current_player_index].name}'s turn.")
        elif card.value == CardValue.SKIP.value:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            print(f"{self.players[self.current_player_index].name} is skipped. Next player's turn.")

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
    import os
    os.system('clear')

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
                card_to_play = game.players[game.current_player_index].hand[int(index)]
                color_choice = None
                if card_to_play.color == CardColor.BLACK.value:
                    color_choice = input("Choose a color (RED, GREEN, BLUE, YELLOW): ").upper()
                    if color_choice not in ColorEnum.__members__:
                        raise ValueError("Invalid color choice. Please choose from RED, GREEN, BLUE, YELLOW.")
                print(f"Attempting to play: Card({ColorEnum[card_to_play.color].value}{card_to_play.value}{Fore.RESET})")
                print(game.play_card(card_to_play, color_choice=color_choice))
                break
            except ValueError as e:
                print(Fore.RED + str(e) + Fore.RESET)
            except IndexError as e:
                print(Fore.RED + "Invalid Index" + Fore.RESET)
        os.system('clear')
    print(game.check_winner())
    print("Game Over!")

