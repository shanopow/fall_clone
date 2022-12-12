# This file is to contain misc items that do not fit into any other files
# This means things like traps, enemies, and global events that have many effects
# My ID allocator is here, maybe clean this up later?

import copy
import random

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

# Function for making deepcopies needed to populate a single room
def populater(holder, to_merge, form_list):
    for item in to_merge:
        new_object = copy.deepcopy(form_list[item])
        new_object.xpos = int(to_merge[item][0])
        new_object.ypos = int(to_merge[item][1])
        holder.append(new_object)
    return holder
# IDs
# form_id run once at the start when we init each template, eg each ("Trader Joe") Npc
def form_id_alloc(item, counter):
    item.form_id = counter
    return