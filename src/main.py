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
def play_card(card_index: Annotated[int, Field(description="Index of the card to play")], color_choice: Annotated[Optional[str], Field(description="Color choice if the card is a wild card (optional)")] = None) -> str:
    """Play a card from the current player's hand."""
    try:
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