# File imports
from map_builder import *
from player_actions import *
from npc_actions import *
from world_actions import *

# Module imports
from os import system, name
from colorama import init, Fore, Back, Style
from getch import getch
import ctypes
import time
import sys
from random import *

# Colorama
init(autoreset=True)

# Fullscreen
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
hWnd = user32.GetForegroundWindow()
user32.ShowWindow(hWnd, SW_MAXIMISE)

# Where the fun begins
# Initials
dweller = Player("Shane", 100, 0, 0, 0, 0, "x")
holdy = [50, 50, 50, 40, 10, 30]

# FOR FIXES RELATED TO ID
# NEED TWO ID TYPES, BASE ID AND REF ID
# BASE ID IS FOR THE GENERIC TEMPLATE, IE ALL "APPLE" HAVE SAME BASE ID
# REF ID IS FOR EACH INDIVIDUAL OBJECT, IE ALL "APPLE" HAVE DIFFERENT REF ID
# BOTH SHOULD BE ASSIGNED AUTOMATICALLY BY THE GENERATOR FOR OBJECTS, NEVER HARD SET SO CAN ADD AS MANY AS WANT WITHOUT OVERLAP
# FOR REF ID, IF NOT PRE_LOADED ITEM, THEN DYNAMICALLY ALLOCATE IT A REF_ID WITH STARTING CHARS "FF", WE CAN THEN EASILY CHECK IF WAS DYNAMICALLY GENERATED

# when dialogue expanded, move to seperate method as will dynamically change through interaction
test_vault = norm_builder(holdy)
guide = Npc("The Guide", 4, 1, True, "passive", "G", ["Hello, this is dummy text", "This is the second line"])
guard = Npc("Guard", 2, 2, False, "neutral", "1")
trader = Npc("Trader Joe", 4, 2, True, "passive", "R", ["Welcome Sir!", "I have the lowest prices around."], "trader", {"apple": 4, "banana": 3, "plum": 6})

# ID is last int here
# ID is kind of pointless, maybe make id system like fnv? Investigate further
spiky = Trap("Spike Trap", 8, 3, 10, "S", 10, True)
death_item = Trap("Trap of Doom", 10, 1, 100 ,"P", 1, False)
vault_details = [dweller, guide, trader, guard, spiky, death_item]
vault_sprinkler(vault_details, test_vault)

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