# File Imports
from save_manager import *

# Module Imports
from colorama import Fore, Back, Style
from os import system
import ctypes
import random
import json

# A representation of a room, only contains all the doors as data so we can link them
class minimapNode(object):
    def __init__(self, vault):
        self.doors_to = {}
        count = 0
        for line in vault:
            for cell in line:
                if cell.item_at != None:
                    if cell.item_at.form_id == "d":
                        self.current_room = cell.item_at.current_room 
                        self.doors_to[count] = cell.item_at.door_to
                        count += 1   

    def __str__(self):
        hold = self.current_room + ": Room\n"
        for item in self.doors_to:
            hold = hold + self.doors_to[item] + "\n"
        return hold

class Door(object):
    def __init__(self, xpos, ypos, door_to, current_room):
        self.xpos = xpos
        self.ypos = ypos
        self.door_to = door_to
        self.icon = "D"
        self.current_room = current_room
        self.form_id = "d"
    
    def __str__(self):
        return ("Door to " + self.door_to)

class Cell(object):
    def __init__(self, y, x, icon, item_at, second_holder=None):
        self.xpos = x
        self.ypos = y
        self.item_at = item_at
        self.icon = icon
        # We use for only in vault_updater, is a holder attribute for the player and other objects to layer
        self.second_holder = second_holder

def player_sight(vault):
    print(Fore.GREEN + "You can see:")
    for line in vault:
        for cell in line:
            if cell.item_at != None:
                print(cell.item_at)
        

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
        player.location = "????"
        room[player.ypos][player.xpos].item_at = player
        return room
    
    else:
        # used a door
        # going to look through each cell for the door to place the player at
        for line in room:
            for cell in line:
                if cell.item_at is not None and cell.item_at.icon == "D":
                    # found the door in the room
                    # used its name to put the player location in the room too
                    player.location = cell.item_at.current_room
                    if cell.item_at.door_to == prev_room.current_room:
                        # found the door linked to prev room
                        # now orient the player using the direction of door in the new room
                        player.xpos = cell.xpos
                        player.ypos = cell.ypos
                        cell.second_holder = cell.item_at
                        cell.item_at = player
                        return room

# Used in vault_updater / enemy movement for after direction has been determined 
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
    
    elif vault[ydir][xdir].item_at.form_id[0] == "e" and not to_move.form_id[0] == "e":
        #combat is done here with normal enemies
        enemy_list = {}
        counter = 0
        for line in vault:
            for cell in line:
                if cell.item_at is not None:
                    if cell.item_at.form_id[0] == "e":
                        counter += 1
                        enemy_list[counter] = cell.item_at
        vault = combat_manager(vault, to_move, enemy_list, True)
    elif vault[ydir][xdir].item_at.form_id[0] == "n":
        # Npcs go here
        vault[ydir][xdir].item_at.interacted(to_move)
    
    return vault


# Uses move_calc above
# Should be ran when wants to move something, mainly a player object in array
# In future, should make projectile function a separate object than this function
def vault_updater(vault, to_move, dir):
    # Vertical
    if dir in "ws":
        if dir == "w":
            vault = move_calc(vault, to_move, to_move.xpos, to_move.ypos - 1)
        elif dir == "s":
            vault = move_calc(vault, to_move,to_move.xpos, to_move.ypos + 1)

    # Horizontal
    elif dir in "ad":
        if dir == "d":
            vault = move_calc(vault, to_move, to_move.xpos + 1, to_move.ypos)
        elif dir == "a":
            vault = move_calc(vault, to_move,  to_move.xpos - 1, to_move.ypos)
    
    # Enemies time for movement
    if type(vault) == list:
        for line in vault:
            for cell in line:
                if cell.item_at != None:
                    if cell.item_at.form_id[0] == "e":
                        if cell.item_at.moved is False:
                            # When we find an enemy who can move, update its movement
                            vault = cell.item_at.movement(to_move, vault)
                        else:
                            cell.item_at.moved = False
    return vault

# Shows vault, ran once after each update
def vault_shower(vault, player):
    longest = 0
    for line in vault:
        if len(line) > longest:
            longest = len(line)

    print(Fore.RED + player.location)
    print(Fore.CYAN + Back.CYAN + " " * (2 + longest))
    for count, line in enumerate(vault):
        print(Fore.CYAN + Back.CYAN + " ", end="")
        holder = ""
        for item in line:
            # All the items in each line
            if item.item_at != None:
                if "t" == item.item_at.form_id[0]:
                    if item.item_at.is_hidden == True:
                        # make the trap hidden
                        holder += " "
                    else:
                        # normal
                        holder += Fore.RED + item.item_at.icon 
                
                elif "p" == item.item_at.form_id[0]:
                    holder += Fore.YELLOW + item.item_at.icon
                
                elif "e" == item.item_at.form_id[0]:
                    holder += Fore.RED + item.item_at.icon

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

def combat_manager(vault, dweller, enemy_list, player_turn):
    #  Show layout of combat board
    enemy_remover = []
    player_turn = True
    while enemy_list != {}:
        print(Fore.CYAN + ("_" * 20))
        print("You can see:")
        for count, enemy in enemy_list.items():
            print(str(count) + ": ", end="")
            print(enemy)
        
        if player_turn:
            player_turn = False
            print("Choose one to attack: ")
            chose_wrong = True
            
            while chose_wrong:
                try:
                    attack_choice = int(input())
                    if attack_choice in enemy_list.keys():
                        chose_wrong = False
                    else:
                        print(Fore.RED + "Please enter a valid enemy to attack.")
                except ValueError:
                    print(Fore.RED + "Please enter a valid enemy to attack.")
            
            location_picked = True
            valid_locations = ["head", "left arm", "right arm", "chest", "right leg", "left leg"]
            
            while location_picked:
                print("Please enter where you want to hit:")
                location_ans = input()
                if location_ans.lower() in valid_locations:
                    location_picked = False
                else:
                    print(Fore.RED + "Please enter a valid location on the body")        
            
            ret_data = dweller.attack(enemy_list[attack_choice], location_ans)
            # When an enemy has been destroyed
            if ret_data[2]:
                enemy_remover.append(enemy_list[attack_choice])
                enemy_list.pop(attack_choice)

        else:
            # enemy turn to attack the player
            for enemy in enemy_list.values():
                print(Fore.RED + enemy.name + " is going to attack!")
                ret_data = enemy.attack(dweller, "body")
            player_turn = True
        # Printing events that happened at end of turn
        
        for log in ret_data[1]:
            print(log)
        a = input()
    
    # Remove all enemies from json and map now
    for item in enemy_remover:
        vault[item.ypos][item.xpos].item_at = None
        file_modifier("", enemy_remover, "local_assets/maps.json", dweller.location)
    return vault