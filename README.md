# SimpleMUD

This repository contains a small text-based dungeon game written in Python. The game is designed to run locally in a terminal and does not require any network connection.

## Running the Game

Ensure you have Python 3 installed. To start the game, run:

```bash
python3 simple_mud.py
```

You will be prompted to enter a name and choose a class (`warrior`, `wizard`, or `rogue`). Then explore the four-room dungeon, fight wandering enemies, and try to survive. The game runs entirely offline using only the Python standard library.

### Controls

- `go <direction>` &ndash; Move to an adjacent room (north, south, east, west where available).
- `attack` &ndash; Attack an enemy in the current room.
- `look` &ndash; Re-describe your current surroundings.
- `help` &ndash; Show available commands.
- `quit` &ndash; Exit the game.

Enemies move after your turn, so stay alert!
