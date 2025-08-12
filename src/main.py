from fastmcp import FastMCP
from typing import Annotated, Optional
from pydantic import Field
from game import UnoGame, Player

mcp = FastMCP("Uno Card Game MCP 🎲")

game = UnoGame([Player(name="User"), Player(name="LLM")])

@mcp.tool(description="Get the current player's information.")
def get_current_player_info() -> str:
    """Get the current player's information."""
    return game.get_current_player_info(player_name=False)

@mcp.tool(description="Play a card from the current player's hand.")
def play_card(card_color: Annotated[str, Field(description="Color of the Card to play (e.g. RED, GREEN, BLUE, YELLOW, BLACK)")],
            card_value: Annotated[str, Field(description="Value of the Card to play (e.g. 0, 1, 2, ..., Skip, Reverse, Draw Two, Wild, Wild Draw Four)")],
            color_choice: Annotated[Optional[str], Field(description="Color choice if the card is a wild card (optional)")] = None) -> str:
    """Play a card from the current player's hand."""
    try:
        card_index = -1
        for i, card in enumerate(game.players[game.current_player_index].hand):
            if card.color == card_color and card.value == card_value:
                card_index = i
                break
        if card_index == -1:
            return "Error: Card not found in your hand."
        game.verif_and_play(card_index, color_choice)
        return "Card played successfully. End of your turn."
    except ValueError as e:
        return f"Error: {str(e)}"
    except IndexError:
        return "Error: Invalid card index."

@mcp.tool(description="Draw a card for the current player.")
def draw_card() -> str:
    """Draw a card for the current player."""
    try:
        game.draw_card()
        return "Card drawn successfully."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")