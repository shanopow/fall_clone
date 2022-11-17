# Module Imports
from colorama import Fore, Back, Style
import ctypes

class Cell(object):
    def __init__(self, y, x, terrain):
        self.xpos = x
        self.ypos = y
        self.terrain = terrain

# For building normal vaults,
# Ran only once here, need separate function to update vaults
# MOVE THIS OUT OF VAULT SHOWER CYCLE, CALLED TOO MANY TIMES
def norm_builder(dims, dweller):
    new_map = []
    i = 0
    while i < len(dims):
        new_line = []
        j = 0
        while j < dims[i]:
            # Find dweller position in vault
            if i == dweller.ypos and j == dweller.xpos:
                new_cell = Cell(i, j, "x")
            else:
                new_cell = Cell(i, j, " ")
            new_line.append(new_cell)
            j += 1
        new_map.append(new_line)
        i += 1
    return new_map

def vault_updater(vault):
    return
# Shows vault, ran a lot, once after each update
def vault_shower(taken, pre_spacing):
    longest = 0
    print()
    for line in taken:
        if len(line) > longest:
            longest = len(line)
    
    print(Fore.CYAN + Back.CYAN + " " * (2 + longest))
    for count, line in enumerate(taken):
        holder = ""
        for item in line:
            holder += item.terrain
        print(Fore.CYAN + Back.CYAN + (" " * pre_spacing[count]), end="")
        print(holder, end="")
        print(Fore.CYAN + Back.CYAN + (" " * (1 + longest - len(line))))
    print(Fore.CYAN + Back.CYAN + " " * (2 + longest))