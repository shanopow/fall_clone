# Module Imports
from colorama import Fore, Back, Style
import ctypes

class Cell(object):
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        

def vault_builder(dim_row, dim_col):
    new_map = []
    i = 0
    while i < dim_row:
        new_line = []
        j = 0
        while j < dim_col:
            new_cell = Cell(i, j, "o")
            new_line.append(new_cell)
            j += 1
        new_map.append(new_line)
        i += 1
    return new_map

def vault_shower(taken):
    print(Fore.CYAN + Back.CYAN + "X" * (2 + len(taken[0])))
    for line in taken:
        holder = ""
        for item in line:
            holder += item.terrain
        print(Fore.CYAN + Back.CYAN + "X", end="")
        print(holder, end="")
        print(Fore.CYAN + Back.CYAN + "X")
    print(Fore.CYAN + Back.CYAN + "X" * (2 + len(taken[0])))