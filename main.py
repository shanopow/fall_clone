# File imports
from map_builder import *
from player_actions import *
from npc_actions import *

# Module imports
from os import system, name
from colorama import init, Fore, Back, Style
from getch import getch
import ctypes
import time
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

# Repeat, keypresses
print("\033[2J")

# npc junk, replace soon
# maybe make its icon better system as can get messy
# need to hold icons along with id in dict so we can reference them quickly
# when dialogue expanded, move to seperate method as will dynamically change through interaction
test_vault = norm_builder(holdy)    
guide = Npc("The Guide", 4, 1, True, "passive", "*", 1, ["Hello, this is dummy text", "This is the second line"])
guard = Npc("Guard", 2, 2, False, "neutral", "1", 2)
vault_details = [dweller, guide, guard]
vault_sprinkler(vault_details, test_vault)

while True:
    vault_shower(test_vault)
    key = getch()
    key = str(key)
    key=key.replace("b", "")
    key=key.replace("'", "")
    key=key.replace("'", "")

    # Test, move one to right then redraw
    could_move = dweller.move_choice(key, test_vault)
    if could_move:
        test_vault = vault_updater(test_vault, dweller, key)
    time.sleep(0.03)
    print("\033[2J")