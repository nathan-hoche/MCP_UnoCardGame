from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
import chess

mcp = FastMCP("Uno Card Game MCP 🎲")

BOARD = chess.Board()

@mcp.tool(description="Get the current state of the chess board.")
def get_board(fen_format:Annotated[bool, Field(description="If True return the board in the fen format (default: False)")]=False) -> str:
    """Get the current state of the chess board."""
    return BOARD.fen() if fen_format else str(BOARD)

@mcp.tool(description="Make a move on the chess board using standard algebraic notation.")
def make_move(san_move: Annotated[str, Field(description="Move to make in the SAN format")]) -> str:
    """Make a move on the chess board using standard algebraic notation."""
    try:
        BOARD.push_san(san_move)
    except chess.InvalidMoveError:
        return f"{san_move} is not a valid move; please provide a valid move in standard algebraic notation."
    except chess.IllegalMoveError:
        return f"{san_move} is an illegal move; please provide a legal move in standard algebraic notation."
    except chess.AmbiguousMoveError:
        return f"{san_move} is an ambiguous move; please provide a disambiguated move in standard algebraic notation."
    return f"Move {san_move} has been made. Current board state: {BOARD.fen()}"

@mcp.tool(description="Get all legal moves from the current position.")
def get_legal_moves() -> str:
    """Get all legal moves from the current position."""
    legal_moves = [move.uci() for move in BOARD.legal_moves]
    if not legal_moves:
        return "There are no legal moves available."
    return f"Legal moves: {', '.join(legal_moves)}"

@mcp.tool(description="Check the current game status.")
def check_game_status() -> str:
    """Check the current game status."""
    if BOARD.is_checkmate():
        return "Checkmate! The game is over."
    elif BOARD.is_stalemate():
        return "Stalemate! The game is drawn."
    elif BOARD.is_insufficient_material():
        return "Insufficient material! The game is drawn."
    elif BOARD.is_seventyfive_moves():
        return "Seventy-five moves rule! The game is drawn."
    elif BOARD.is_fivefold_repetition():
        return "Fivefold repetition! The game is drawn."
    elif BOARD.is_check():
        return "Check! The king is in check."
    else:
        return "The game is ongoing."

@mcp.tool(description="Reset the chess board to the starting position.")
def reset_board() -> str:
    """Reset the chess board to the starting position."""
    global BOARD
    BOARD = chess.Board()
    return "The chess board has been reset to the starting position."

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")