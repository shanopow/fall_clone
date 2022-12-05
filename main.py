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

# This will need to be a json later
holdy = [50, 50, 50, 40, 10, 30]
test_vault = norm_builder(holdy)

# FOR FIXES RELATED TO ID
# NEED TWO ID TYPES, BASE ID AND REF ID
# BASE ID IS FOR THE GENERIC TEMPLATE, IE ALL "APPLE" HAVE SAME BASE ID
# REF ID IS FOR EACH INDIVIDUAL OBJECT, IE ALL "APPLE" HAVE DIFFERENT REF ID
# REF ID MADE AFTER EACH DEEPCOPY, STICKS WITH THAT ONE ITEM THEN

# Reading from the json files
# mega_list holds each possible object in the game
# index based on form_id
# should be no dupes here at all
traps = object_builder("traps.json", "__main__.Trap", "traps")
npcs = object_builder("npcs.json", "__main__.Npc", "npcs")
dweller = Player("Shane", 100, 0, 0, 0, 0, "x", "p1")
npcs.append(dweller)
mega_list = final_object_builder(traps + npcs)

first_room = populater(["t1", "t2", "n1", "n2", "n3"], mega_list)
first_room[0] = dweller
vault_sprinkler(first_room, test_vault)

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