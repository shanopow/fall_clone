# This file is to contain misc items that do not fit into any other files
# This means things like traps, enemies, and gloabl events that have many effects

class Trap(object):
    def __init__(self, name, xpos, ypos, damage, icon , id, is_hidden=False):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.damage = damage
        self.icon = icon
        self.id = id
        self.is_hidden = is_hidden
    
    def interacted(self, dweller):
        dweller.health -= self.damage
        self.is_hidden = False
        print("There was a {} on this tile!".format(self.name))
        print("You now have {} hp!".format(dweller.health))
        a = input()