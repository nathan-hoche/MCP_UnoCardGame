# MCP Uno Card Game 🎲

# Introduction

This project is a simple MCP to enable an LLM to Uno Card Game. It is designed to al
> [!IMPORTANT]
> This project is a small project to demonstrate the use of MCP with LLMs, it does not includlow a language model to play Uno with a user by providing a set of tools that the model can use to interact with the game.

> [!NOTE]
> The game processing is handle by the MCP, so the user need to interact to play is turn using an MCP client. (e.g. `MCP Inspector`)


> [!IMPORTANT]
> This project is a small project to demonstrate the use of MCP with LLMs, it does not include an implementation of session management or user authentication. It is recommended to use this project as a starting point for your own projects and to implement your own session management and user authentication if needed.

# Usage

To use this project, you will first need to install the required dependencies. You can do this by running:

```bash
pip install -r requirements.txt
```

Then, you can run the MCP server using:

```bash
python src/main.py
```

> [!NOTE]
> The MCP server use the `Streamable-http` for the communication, this can be changed in the `main.py` file.


# List of tools

| Tool Name | Arguments | Description |
| --- | --- | --- |
| get_current_player_info | / | Get the current player's information. |
| play_card | card_color, card_value, color_choice (Optional) | Play a card from the current player's hand. |
| draw_card | / | Draw a card for the current player. |


> [!NOTE]
> After playing a card, the MCP will automatically update the game state and switch to the next player. The user can then use the `get_current_player_info` tool to get the updated game state.

> [!WARNING]
> The user can also use the `draw_card` tool to draw a card for the current player if they cannot play a card. The player need to play a card after drawing a card, if they can. If they cannot play a card, they need to continue to draw cards until they can play a card or the deck is empty.

