# File imports
from map_builder import *
from player_actions import *

# Module imports
from colorama import init, Fore, Back, Style
from getch import getch
import ctypes
import time
# Colorama
init(autoreset=True)

# Function for clearing screen
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# Fullscreen
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
hWnd = user32.GetForegroundWindow()
user32.ShowWindow(hWnd, SW_MAXIMISE)

# Where the fun begins
# Initials
dweller = Player("Shane", 100, 0, 0, 0, 0)
holdy = [30, 10, 14, 21, 12, 8, 2]
# Repeat, keypresses
while True:
    a = norm_builder(holdy, dweller)
    vault_shower(a, pre_spacing)
    key = getch()
    key = str(key)
    key=key.replace("b","")
    key=key.replace("'","")
    key=key.replace("'","")

    # Test, move one to right then redraw
    dweller.move_choice(key, a)
    time.sleep(0.05)
    print("\033[2J")