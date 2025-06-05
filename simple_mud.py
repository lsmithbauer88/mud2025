#!/usr/bin/env python3

import random
import textwrap

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.neighbors = {}

    def connect(self, direction, other):
        self.neighbors[direction] = other

class Character:
    def __init__(self, name, role, hp, atk):
        self.name = name
        self.role = role
        self.hp = hp
        self.atk = atk
        self.room = None

class Enemy:
    def __init__(self, name, hp, atk, room):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.room = room

    def is_alive(self):
        return self.hp > 0

    def move(self):
        if self.room.neighbors:
            self.room = random.choice(list(self.room.neighbors.values()))

class Game:
    def __init__(self):
        self.rooms = self.build_rooms()
        self.player = self.create_player()
        self.enemies = self.spawn_enemies()
        self.turn = 0

    def build_rooms(self):
        entrance = Room('Entrance', 'You stand at the dungeon entrance. A dark hall lies north.')
        hall = Room('Hall', 'A damp corridor stretches before you.')
        armory = Room('Armory', 'Old weapons litter the floor.')
        library = Room('Library', 'Dusty books fill ancient shelves.')

        entrance.connect('north', hall)
        hall.connect('south', entrance)
        hall.connect('east', armory)
        hall.connect('west', library)
        armory.connect('west', hall)
        library.connect('east', hall)

        return {
            'entrance': entrance,
            'hall': hall,
            'armory': armory,
            'library': library,
        }

    def create_player(self):
        name = input('Enter your character\'s name: ')
        role = ''
        while role not in ['warrior', 'wizard', 'rogue']:
            role = input('Choose a class (warrior/wizard/rogue): ').lower()
        if role == 'warrior':
            hp, atk = 15, 3
        elif role == 'wizard':
            hp, atk = 10, 4
        else:
            hp, atk = 12, 3
        player = Character(name, role, hp, atk)
        player.room = self.rooms['entrance']
        return player

    def spawn_enemies(self):
        enemies = [
            Enemy('Goblin', 5, 2, self.rooms['hall']),
            Enemy('Skeleton', 5, 2, self.rooms['armory']),
        ]
        return enemies

    def living_enemies_in_room(self, room):
        return [e for e in self.enemies if e.room == room and e.is_alive()]

    def describe_room(self):
        r = self.player.room
        print(f"\n== {r.name} ==")
        for line in textwrap.wrap(r.description, width=60):
            print(line)
        if r.neighbors:
            print('Exits:', ', '.join(r.neighbors.keys()))
        enemies = self.living_enemies_in_room(r)
        for e in enemies:
            print(f'A {e.name} is here!')

    def process_command(self, cmd):
        if cmd.startswith('go '):
            direction = cmd.split(' ', 1)[1]
            if direction in self.player.room.neighbors:
                self.player.room = self.player.room.neighbors[direction]
                print(f'You move {direction}.')
            else:
                print("You can't go that way.")
        elif cmd == 'attack':
            enemies = self.living_enemies_in_room(self.player.room)
            if enemies:
                target = enemies[0]
                target.hp -= self.player.atk
                print(f'You hit the {target.name}! It has {target.hp} hp left.')
                if target.hp <= 0:
                    print(f'The {target.name} is defeated!')
            else:
                print('No enemy to attack.')
        elif cmd == 'help':
            print('Commands: go <direction>, attack, help, quit')
        elif cmd == 'quit':
            return False
        else:
            print('Unknown command. Type "help".')
        return True

    def enemy_actions(self):
        for e in self.enemies:
            if not e.is_alive():
                continue
            if e.room == self.player.room:
                self.player.hp -= e.atk
                print(f'The {e.name} hits you! You have {self.player.hp} hp.')
            else:
                e.move()

    def play(self):
        print('\nWelcome to SimpleMUD! Type "help" for commands.')
        running = True
        while running and self.player.hp > 0:
            self.describe_room()
            cmd = input('> ').strip().lower()
            running = self.process_command(cmd)
            if not running:
                break
            self.enemy_actions()
            if all(not e.is_alive() for e in self.enemies):
                print('You defeated all enemies. Victory!')
                break
        if self.player.hp <= 0:
            print('You have been defeated...')

if __name__ == '__main__':
    Game().play()
