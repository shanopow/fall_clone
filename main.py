# Not all here are needed, this is to keep track of all needed modules across entre program

# File imports
from map_builder import *
from player_actions import *
from npc_actions import *
from world_actions import *
from json_handler import *

# Module imports
from os import system, name
from colorama import init, Fore, Back, Style
from getch import getch

import random
import ctypes
import time
import sys
import json
import copy

# Colorama
init(autoreset=True)

# Fullscreen
win_lin = input("win or lin?")
if win_lin == "win":
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMISE = 3
    hWnd = user32.GetForegroundWindow()
    user32.ShowWindow(hWnd, SW_MAXIMISE)

# Reading from the json files
# mega_list holds each possible object in the game
# index based on form_id
# should never be dupes here
traps = object_builder("traps.json", "__main__.Trap", "traps")
npcs = object_builder("npcs.json", "__main__.Npc", "npcs")
enemies = object_builder("enemies.json", "__main__.Enemy", "enemies")

dweller = Player("Shane", 100, 1, 2, 1, 1, "x", "p1")
players = []
players.append(dweller)
mega_list = final_object_builder(traps + npcs + enemies + players)

# Initial room
room = map_maker("maps.json", "square_room", mega_list)
room = player_placer(dweller, None, room)

print("Choose the type of clearing")
print("cls / other")
a = input()
if a == "cls":
    system('cls')
else:
    print("\033[2J")

just_entered = True
# hard-coded ends here

# Core turn loop
while True:
    if just_entered:
        player_sight(room)
    vault_shower(room)
    key = getch()
    key = str(key)
    key = key.replace("b", "")
    key = key.replace("'", "")
    key = key.replace("'", "")

    could_move = dweller.move_choice(key, room, mega_list)
    if could_move:
        # keep copy of old room if we need to use door
        room = vault_updater(room, dweller, key)
        if "list" not in str(type(room)):
            # door used
            just_entered = True
            old_room = copy.deepcopy(room)
            room = map_maker("maps.json", room.door_to, mega_list)
            room = player_placer(dweller, old_room, room)
        else:
            just_entered = False

    if a == "cls":
        system('cls')
    else:
        print("\033[2J")