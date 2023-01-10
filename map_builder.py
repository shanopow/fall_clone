# Module Imports

from colorama import Fore, Back, Style
import ctypes
import random

class Door(object):
    def __init__(self, xpos, ypos, door_to, current_room):
        self.xpos = xpos
        self.ypos = ypos
        self.door_to = door_to
        self.icon = "D"
        self.current_room = current_room

class Cell(object):
    def __init__(self, y, x, icon, item_at, second_holder=None):
        self.xpos = x
        self.ypos = y
        self.item_at = item_at
        self.icon = icon
        # We use for only in vault_updater, is a holder attribute for the player and other objects to layer
        self.second_holder = second_holder

# For building normal vaults, adds in all the cells with empty item_at attributes
def norm_builder(dims):
    new_map = []
    i = 0
    door_count = 0
    for line in dims:
        new_line = []
        j = 0
        for spot in line:
            if spot == 1:
                # Walls
                # █
                new_cell = Cell(i, j, " ", None)
            else:
                new_cell = Cell(i, j, "█", None)
            new_line.append(new_cell)
            j += 1
        new_map.append(new_line)
        i += 1
    return new_map

# makes door objects
# twin to vault_sprinkler
def door_maker(details, doors, map_holder, map_name):
    for item in doors:
        new_door = Door(int(doors[item].split(",")[0]), int(doors[item].split(",")[1]), item, map_name)
        details.append(new_door)
    return details

# Sprinkles objects onto the vault cells, replacing the none types on their item_at attribute with the new object
# Use once, directly after norm_builder
def vault_sprinkler(details, vault):
        for item in details:
            for slot in vault[item.ypos]:
                if slot.xpos == item.xpos:
                    slot.item_at = item
                    break

# For placing the player onto the map, will be ran after each room generation
def player_placer(player, prev_room, room):
    if prev_room is None:
        # just spawned, ran once at creation
        player.xpos = 0
        player.ypos = 0
        room[player.ypos][player.xpos].item_at = player
        return room
    
    else:
        # used a door
        # going to look through each cell for the door to place the player at
        for line in room:
            for cell in line:
                if cell.item_at is not None and cell.item_at.icon == "D":
                    # found the door in the room
                    if cell.item_at.door_to == prev_room.current_room:
                        # found the door linked to prev room
                        # now orient the player using the direction of door in the new room
                        player.xpos = cell.xpos
                        player.ypos = cell.ypos
                        cell.second_holder = cell.item_at
                        cell.item_at = player
                        return room

# Used in vault_updater for after direction has been determined 
def move_calc(vault, to_move, xdir, ydir):
    if vault[ydir][xdir].item_at == None:
        # Normal movement
        if vault[to_move.ypos][to_move.xpos].second_holder is not None:
            # If we are moving off of a door
            vault[to_move.ypos][to_move.xpos].item_at = vault[to_move.ypos][to_move.xpos].second_holder
            vault[to_move.ypos][to_move.xpos].second_holder = None
        else:
            vault[to_move.ypos][to_move.xpos].item_at = None
        
        vault[ydir][xdir].item_at = to_move
        to_move.ypos = ydir
        to_move.xpos = xdir
    
    elif vault[ydir][xdir].item_at.icon == "D":
        #Moving into a door here
        return vault[ydir][xdir].item_at
    else:
        vault[ydir][xdir].item_at.interacted(to_move)
        # Npcs go here

    return vault


# Uses move_calc above
# Should be ran when wants to move something, mainly a player object in array
# In future, should make projectile function a separate object than this function
def vault_updater(vault, to_move, dir):
    # Vertical
    if dir in "ws":
        if dir == "w":
            vault = move_calc(vault, to_move, to_move.xpos, to_move.ypos - 1)
            return vault
        
        elif dir == "s":
            vault = move_calc(vault, to_move,to_move.xpos, to_move.ypos + 1)
            return vault

    # Horizontal
    elif dir in "ad":
        if dir == "d":
            vault = move_calc(vault, to_move, to_move.xpos + 1, to_move.ypos)
            return vault
                
        elif dir == "a":
            vault = move_calc(vault, to_move,  to_move.xpos - 1, to_move.ypos)
            return vault


# Shows vault, ran once after each update
def vault_shower(vault):
    longest = 0
    for line in vault:
        if len(line) > longest:
            longest = len(line)

    print(Fore.CYAN + Back.CYAN + " " * (2 + longest))
    for count, line in enumerate(vault):
        print(Fore.CYAN + Back.CYAN + " ", end="")
        holder = ""
        for item in line:
            # All the items in each line
            if item.item_at != None:
                if "Trap" in str(type(item.item_at)):
                    if item.item_at.is_hidden == True:
                        holder += " "
                    else:
                        holder += Fore.RED + item.item_at.icon 
                elif "Player" in str(type(item.item_at)):
                    holder += Fore.YELLOW + item.item_at.icon
                else:
                    holder += Fore.WHITE + item.item_at.icon
            else:
                if item.icon != " ":
                    # impassable
                    holder += (Fore.CYAN + item.icon)
                else:
                    holder += item.icon
        print(holder, end="")
        print(Fore.CYAN + Back.CYAN + (" " * (1 + longest - len(line))))
    print(Fore.CYAN + Back.CYAN + " " * (2 + longest))