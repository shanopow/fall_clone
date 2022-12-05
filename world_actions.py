# This file is to contain misc items that do not fit into any other files
# This means things like traps, enemies, and gloabl events that have many effects
# My ID allocator is here, maybe clean this up later?

class Trap(object):
    def __init__(self, name, xpos, ypos, damage, icon ,is_hidden=False):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.damage = damage
        self.icon = icon
        self.is_hidden = is_hidden
    
    def interacted(self, dweller):
        dweller.health -= self.damage
        self.is_hidden = False
        print("There was a {} on this tile!".format(self.name))
        print("You now have {} hp!".format(dweller.health))
        a = input()

# opens and reads file into list, used in normal object builder, DO NOT USE ALONE
def file_reader(file_name):
    file = open(file_name, "r")
    raw_data = file.readlines()
    file.close()
    return raw_data

# for converting name of class in str to actual class, used in normal object builder, DO NOT USE ALONE
def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m


# IDs
# form_id run once at the start when we init each template, eg each ("Trader Joe") Npc
def form_id_alloc(item, counter)
    item.form_id = counter
    return counter += 1
def ref_id_alloc(item)
    
    return
# 3.1, 3.5