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
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
hWnd = user32.GetForegroundWindow()
user32.ShowWindow(hWnd, SW_MAXIMISE)

# Clearing Option
#system('cls')
print("\033[2J")


# Main Menu
# For skipping
norm_user = False
if norm_user:
    main_acter()
    system('cls')
    #print("\033[2J")

# Reading from the json files
# mega_list holds each possible object in the game
# index based on form_id
# should never be dupes here
traps = object_builder("assets/traps.json", "__main__.Trap", "traps")
npcs = object_builder("assets/npcs.json", "__main__.Npc", "npcs")
enemies = object_builder("assets/enemies.json", "__main__.Enemy", "enemies")
weapons = object_builder("assets/weapons.json", "__main__.Weapon", "weapons")
armour = object_builder("assets/armour.json", "__main__.Armour", "armour")

# Final list of all objects in game
mega_list = final_object_builder(traps + npcs + enemies + weapons + armour)
dweller = Player("Shane", 100, 1, 2, 1, 1, "x", "p001", ["w000", "a000"], mega_list, [5,5,5,5,5,5,5])
mega_list[dweller.form_id] = dweller

# Initial room
room = map_maker("assets/maps.json", "square_room", mega_list)
room = player_placer(dweller, None, room)

just_entered = True
# hard-coded ends here

# Core turn loop
while True:
    if just_entered:
        player_sight(room)
    vault_shower(room, dweller)
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
            # room variable is now the door we used
            just_entered = True
            old_room = copy.deepcopy(room)
            room = map_maker("assets/maps.json", room.door_to, mega_list)
            room = player_placer(dweller, old_room, room)
        else:
            just_entered = False

    #system('cls')
    print("\033[2J")