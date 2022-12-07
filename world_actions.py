# This file is to contain misc items that do not fit into any other files
# This means things like traps, enemies, and gloabl events that have many effects
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
def populater(holder, form_list, pos_list):
    deep_room = {}
    for count, item in enumerate(holder):
        slotted = False
        i = 0
        while slotted is False:
            if i > 100:
                slotted = True
            # pos 1 is always allocated to the player, as they always need a spot in room
            ref_id = random.randint(1, 1000)
            if ref_id not in deep_room:
                deep_room[ref_id] = copy.deepcopy(form_list[item])
                deep_room[ref_id].xpos = int(pos_list[count][0])
                deep_room[ref_id].ypos = int(pos_list[count][1])
                slotted = True
            i += 1
    return deep_room

# IDs
# form_id run once at the start when we init each template, eg each ("Trader Joe") Npc
def form_id_alloc(item, counter):
    item.form_id = counter
    return