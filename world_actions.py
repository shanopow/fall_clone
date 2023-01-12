# This file is to contain misc items that do not fit into any other files
# This means things like traps, enemies, and global events that have many effects
# My ID allocator is here, maybe clean this up later?

import copy
import random
from colorama import Fore, Back, Style

class Trap(object):
    def __init__(self, holder):
        #name, xpos, ypos, damage, icon ,is_hidden=False
        self.name = holder[0]
        self.damage = holder[1]
        self.icon = holder[2]
        if holder[3] == "1":
            self.is_hidden = True
        else:
            self.is_hidden = False
        self.form_id = holder[4]

    def interacted(self, dweller):
        dweller.health -= self.damage
        self.is_hidden = False
        print("There was a {} on this tile!".format(self.name))
        print("You now have {} hp!".format(dweller.health))
        a = input()

# Used as startup to main_acter
def main_shower():
    logo = [" ######    #    #       #                 #       ####### #     # #######  ", " #        # #   #       #           ####  #       #     # ##    # #       "," #       #   #  #       #          #    # #       #     # # #   # #        ", " #####  #     # #       #          #      #       #     # #  #  # #####    ", " #      ####### #       #          #      #       #     # #   # # #        ", " #      #     # #       #          #    # #       #     # #    ## #        ", " #      #     # ####### #######     ####  ####### ####### #     # #######  "]
    for line in logo:
        print(Fore.RED + line)
    
    print("\n" * 5)
    print(Fore.GREEN + "Please choose an option below\n")
    print("1: New game")
    print("2: Load Game")
    print("3: Quit")
    user_choice = input()
    return user_choice

# interprets return value from main_shower on main_menu
def main_acter():
    user_input = main_shower()
    if user_input == "1":
        return
    elif user_input == "2":
        return
    else:
        quit()

# Function for making deepcopies needed to populate a single room
def populater(holder, to_merge, form_list):
    for item in to_merge:
        new_object = copy.deepcopy(form_list[to_merge[item]])
        
        new_object.xpos = int(item.split(",")[0])
        new_object.ypos = int(item.split(",")[1])
        
        holder.append(new_object)
    return holder
# IDs
# form_id run once at the start when we init each template, eg each ("Trader Joe") Npc
def form_id_alloc(item, counter):
    item.form_id = counter
    return