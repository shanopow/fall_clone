# JESSE WE NEED DOOR FOR ALL THE MAPS
# MR WHITE YO THE DOORS CANT BE NNPCS MAYBE LINKED LIST?
# MAYBE SPECIAL INTERACTION TYPE FOR NPC "DOOR "
# Not all here are needed, this is to keep track of all nded modules across entre program
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
# should be no dupes here at all
traps = object_builder("traps.json", "__main__.Trap", "traps")
npcs = object_builder("npcs.json", "__main__.Npc", "npcs")
enemies = object_builder("enemies.json", "__main__.Enemy", "enemies")

dweller = Player("Shane", 100, 1, 2, 1, 1, "x", "p1")
npcs.append(dweller)
mega_list = final_object_builder(traps + npcs + enemies)

# done for each room
first_room = populater(["n1", "n2", "n2", "n3"], mega_list, ["44", "00", "20", "34"])
first_room[0] = dweller

chosen = map_maker("maps.json", "hallway")
test_vault = norm_builder(chosen, ["square_room"])
vault_sprinkler(first_room ,test_vault)

print("Choose the type of clearing")
print("cls / other")
a = input()
if a == "cls":
    system('cls')
else:
    print("\033[2J")

while True:
    vault_shower(test_vault)
    key = getch()
    key = str(key)
    key = key.replace("b", "")
    key = key.replace("'", "")
    key = key.replace("'", "")

    could_move = dweller.move_choice(key, test_vault)
    if could_move:
        test_vault = vault_updater(test_vault, dweller, key)
    if a == "cls":
        system('cls')
    else:
        print("\033[2J")