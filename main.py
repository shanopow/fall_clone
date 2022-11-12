# File imports
from map_builder import *
# Module imports
from colorama import init, Fore, Back, Style
import os
import ctypes

# Colorama
init(autoreset=True)

# Fullscreen
user32 = ctypes.WinDLL('user32')
SW_MAXIMISE = 3
hWnd = user32.GetForegroundWindow()
user32.ShowWindow(hWnd, SW_MAXIMISE)


first = vault_builder(45,60)
vault_shower(first)
