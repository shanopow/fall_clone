# Module Imports
from colorama import Fore, Back, Style
import ctypes
import random

class Cell(object):
    def __init__(self, y, x, item_at, second_holder=None):
        self.xpos = x
        self.ypos = y
        self.item_at = item_at
        # we use for only in vault_updater, just holds while player is over object
        self.second_holder = second_holder

# For building normal vaults, adds in all the cells with empty item_at attributes
def norm_builder(dims):
    weights_holder = [10,1]
    choices_holder = [0,1]
    new_map = []
    i = 0
    while i < len(dims):
        new_line = []
        j = 0
        while j < dims[i]:
            new_cell = Cell(i, j, None)
            new_line.append(new_cell)
            j += 1
        new_map.append(new_line)
        i += 1
    return new_map

# Sprinkles objects onto the vault cells, replacing the none types on their item_at attribute with the new object
# Use once, directly after norm_builder
def vault_sprinkler(details, vault):
    for item in details:
        for slot in vault[item.ypos]:
            if slot.xpos == item.xpos:
                slot.item_at = item

# Should be ran when wants to move something, mainly a player object in array
def vault_updater(vault, to_move, dir):
    # Vertical
    if dir in "ws":
        if dir == "w":
            for count, item in enumerate(vault[to_move.ypos]):
                if item.item_at == to_move:
                    if vault[to_move.ypos - 1][count].item_at == None:
                        item.item_at = None
                        to_move.ypos -= 1
                        vault[to_move.ypos][count].item_at = to_move
                    else:
                        vault[to_move.ypos - 1][count].item_at.interacted()
                    return vault
        elif dir == "s":
            for count, item in enumerate(vault[to_move.ypos]):
                if item.item_at == to_move:
                    if vault[to_move.ypos + 1][count].item_at == None:
                        item.item_at = None
                        to_move.ypos += 1
                        vault[to_move.ypos][count].item_at = to_move
                    else:
                        vault[to_move.ypos + 1][count].item_at.interacted()
                    return vault

    # Horizontal
    elif dir in "ad":
        for count, item in enumerate(vault[to_move.ypos]):
            if item.item_at == to_move:
                if dir == "d":
                    if vault[to_move.ypos][count + 1].item_at == None: 
                        item.item_at = None
                        to_move.xpos += 1
                        vault[to_move.ypos][count + 1].item_at = to_move
                    else:
                        vault[to_move.ypos][count + 1].item_at.interacted()
                    return vault
                elif dir == "a":
                    if vault[to_move.ypos][count - 1].item_at == None:
                        item.item_at = None
                        to_move.xpos -= 1
                        vault[to_move.ypos][count - 1].item_at = to_move
                    else:
                        vault[to_move.ypos][count - 1].item_at.interacted()
                    return vault

# Shows vault, ran once after each update
def vault_shower(vault):
    longest = 0
    for line in vault:
        if len(line) > longest:
            longest = len(line)

    print(Fore.CYAN + Back.CYAN + " " * (2 + longest))
    for count, line in enumerate(vault):
        holder = ""
        for item in line:
            if item.item_at != None:
                holder += item.item_at.icon
            else:
                # empty cells
                holder += " "
        print(Fore.CYAN + Back.CYAN + " ", end="")
        print(holder, end="")
        print(Fore.CYAN + Back.CYAN + (" " * (1 + longest - len(line))))
    print(Fore.CYAN + Back.CYAN + " " * (2 + longest))