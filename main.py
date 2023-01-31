# Not all here are needed, this is to keep track of all needed modules across entre program

# File imports
from player_actions import *
from npc_actions import *
from world_actions import *
from json_handler import *
from save_manager import *
from map_builder import *

# Module imports
from os import system, name
from colorama import init, Fore, Back, Style
from getch import getch

from random import randint
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
system('cls')
#print("\033[2J")
# Main Menu
# For skipping
norm_user = True
if norm_user:
    cont_new = main_acter()
    # Should be expnaded to multiple saves
    if cont_new:
        # Set up local files 
        file_deleter("local_assets/maps.json")
        file_mover("assets/maps.json")
    system('cls')
    #print("\033[2J")

# Reading from the json files
# mega_list holds each possible object in the game
# index based on form_id
# should never be dupes here
traps = object_builder("assets/traps.json", "__main__.Trap", "traps")
npcs = object_builder("assets/npcs.json", "__main__.Npc", "npcs")
weapons = object_builder("assets/weapons.json", "__main__.Weapon", "weapons")
armour = object_builder("assets/armour.json", "__main__.Armour", "armour")
traps = object_builder("assets/traps.json", "__main__.Trap", "traps")
quests = object_builder("assets/quests.json", "__main__.Quest", "quests")

animals = object_builder("assets/enemies/animals.json", "__main__.Animal", "animals")
hostiles = object_builder("assets/enemies/hostiles.json", "__main__.Hostile", "hostiles")

# Final list of all objects in game
mega_list = final_object_builder(traps + npcs + animals + hostiles + weapons + armour + quests)

# Player
dweller = Player("Shane", 100, 1, 2, 1, 1, "x", "p001", ["w000", "a000"], mega_list, [5,5,5,5,5,5,5])
mega_list[dweller.form_id] = dweller
# Initial room
curr_area = "vault1"
room = map_maker("local_assets/maps.json", "square room", curr_area, mega_list)
room = player_placer(dweller, None, room)
just_entered = True
# minimap
node_holder = []
#new_node = minimapNode(room)
#node_holder.append(new_node)

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

    could_move = dweller.move_choice(key, room, mega_list, node_holder)
    if could_move:
        # keep copy of old room if we need to use door
        room = vault_updater(room, dweller, key)
        if "list" not in str(type(room)):
            # door used
            # room variable is now the door we used
            just_entered = True
            old_room = copy.deepcopy(room)
            # moving to another area
            if "," in room.door_to:
                curr_area = room.door_to.split(",")
                next_room = curr_area[1]
                curr_area = curr_area[0]
                old_room = None
            else:
                next_room = room.door_to
            room = map_maker("local_assets/maps.json", next_room, curr_area, mega_list)
            room = player_placer(dweller, old_room, room)
            # Minimap
            """new_node = minimapNode(room)
            passed = True
            for node in node_holder:
                if node.current_room == new_node.current_room:
                    passed = False
            if passed:
                node_holder.append(new_node)
            """        
        else:
            just_entered = False

    #system('cls')
    print("\033[2J")