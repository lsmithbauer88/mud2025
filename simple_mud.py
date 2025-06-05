#!/usr/bin/env python3
"""A minimal text-based dungeon crawler."""

import random
import textwrap
from dataclasses import dataclass, field
from typing import Dict, List

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
except ImportError:  # colour is optional
    class _Dummy:
        def __getattr__(self, name: str) -> str:
            return ""

    Fore = Style = _Dummy()

# Directions used in the dungeon
DIRECTIONS = ("north", "south", "east", "west")

@dataclass
class Room:
    """A location in the dungeon."""

    name: str
    description: str
    neighbors: Dict[str, "Room"] = field(default_factory=dict)

    def connect(self, direction: str, other: "Room") -> None:
        """Connect this room to another in the given direction."""
        self.neighbors[direction] = other

@dataclass
class Character:
    """The player's avatar."""

    name: str
    role: str
    hp: int
    atk: int
    room: Room | None = None

@dataclass
class Enemy:
    """A simple hostile creature."""

    name: str
    hp: int
    atk: int
    room: Room

    def is_alive(self) -> bool:
        return self.hp > 0

    def move(self) -> None:
        """Move to a random neighboring room."""
        if self.room.neighbors:
            self.room = random.choice(list(self.room.neighbors.values()))

class Game:
    """Main game controller."""

    def __init__(self) -> None:
        self.rooms = self._build_rooms()
        self.player = self._create_player()
        self.enemies = self._spawn_enemies()

    def _build_rooms(self) -> Dict[str, Room]:
        entrance = Room(
            "Entrance",
            "You stand at the moss-covered mouth of an ancient dungeon. A dark hall beckons to the north."
        )
        hall = Room(
            "Hall",
            "A damp corridor stretches before you. Faint echoes bounce along the stone walls."
        )
        armory = Room(
            "Armory",
            "Rusty blades and dented armour lie scattered in disarray. The air smells of old metal."
        )
        library = Room(
            "Library",
            "Dusty tomes fill towering shelves, their wisdom long forgotten."
        )

        entrance.connect("north", hall)
        hall.connect("south", entrance)
        hall.connect("east", armory)
        hall.connect("west", library)
        armory.connect("west", hall)
        library.connect("east", hall)

        return {
            "entrance": entrance,
            "hall": hall,
            "armory": armory,
            "library": library,
        }

    def _create_player(self) -> Character:
        """Prompt for a name and class, ensuring clear prompts on Windows."""
        print("Welcome to SimpleMUD, a short offline dungeon crawl.")
        print("Strange whispers echo from somewhere below...", flush=True)
        print("Let's create your character.", flush=True)
        name = ""
        while not name:
            name = input("Enter your character's name: ").strip()
        print(flush=True)  # put the next prompt on a new line for clarity

        role = ""
        while role not in {"warrior", "wizard", "rogue"}:
            role = input("Choose a class (warrior/wizard/rogue): ").strip().lower()
        stats = {
            "warrior": (15, 3),
            "wizard": (10, 4),
            "rogue": (12, 3),
        }
        hp, atk = stats[role]
        player = Character(name, role, hp, atk)
        player.room = self.rooms["entrance"]
        return player

    def _spawn_enemies(self) -> List[Enemy]:
        return [
            Enemy("Goblin", 5, 2, self.rooms["hall"]),
            Enemy("Skeleton", 5, 2, self.rooms["armory"]),
        ]

    def _living_enemies_in_room(self, room: Room) -> List[Enemy]:
        return [e for e in self.enemies if e.room == room and e.is_alive()]

    def _describe_room(self) -> None:
        r = self.player.room
        if not r:
            return
        print(Fore.CYAN + f"\n== {r.name} ==" + Style.RESET_ALL)
        for line in textwrap.wrap(r.description, width=60):
            print(line)
        if r.neighbors:
            print("Exits:", ", ".join(r.neighbors.keys()))
        for e in self._living_enemies_in_room(r):
            print(Fore.RED + f"A {e.name} is here!" + Style.RESET_ALL)

    def _move_player(self, direction: str) -> None:
        if direction in self.player.room.neighbors:
            self.player.room = self.player.room.neighbors[direction]
            print(Fore.GREEN + f"You move {direction}." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "You can't go that way." + Style.RESET_ALL)

    def _attack(self) -> None:
        enemies = self._living_enemies_in_room(self.player.room)
        if enemies:
            target = enemies[0]
            target.hp -= self.player.atk
            print(Fore.YELLOW + f"You hit the {target.name}! It has {target.hp} hp left." + Style.RESET_ALL)
            if target.hp <= 0:
                print(Fore.GREEN + f"The {target.name} is defeated!" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "No enemy to attack." + Style.RESET_ALL)

    def _enemy_actions(self) -> None:
        for e in self.enemies:
            if not e.is_alive():
                continue
            if e.room == self.player.room:
                self.player.hp -= e.atk
                print(Fore.RED + f"The {e.name} hits you! You have {self.player.hp} hp." + Style.RESET_ALL)
            else:
                e.move()

    def _process_command(self, cmd: str) -> bool:
        if cmd.startswith("go "):
            direction = cmd.split(" ", 1)[1]
            self._move_player(direction)
        elif cmd == "attack":
            self._attack()
        elif cmd == "look":
            self._describe_room()
        elif cmd == "help":
            print("Commands: go <direction>, attack, look, help, quit")
        elif cmd == "quit":
            return False
        else:
            print('Unknown command. Type "help".')
        return True

    def play(self) -> None:
        print(Fore.CYAN + "\nWelcome to SimpleMUD! Type 'help' for commands." + Style.RESET_ALL)
        running = True
        while running and self.player.hp > 0:
            self._describe_room()
            cmd = input("> ").strip().lower()
            running = self._process_command(cmd)
            if not running:
                break
            self._enemy_actions()
            if all(not e.is_alive() for e in self.enemies):
                print(Fore.GREEN + "You defeated all enemies. Victory!" + Style.RESET_ALL)
                break
        if self.player.hp <= 0:
            print(Fore.RED + "You have been defeated..." + Style.RESET_ALL)

if __name__ == "__main__":
    Game().play()
