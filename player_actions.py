from json_handler import map_maker
from colorama import Fore, Back, Style
from getch import getch

import random
import copy

class Player(object):
    def __init__(self, name, health, xp, rads, xpos, ypos, icon, form_id, inventory, item_list, special):
        # Basic
        self.name = name
        self.health = health
        self.xp = xp
        self.rads = rads
        self.xpos = xpos
        self.ypos = ypos
        self.icon = icon
        self.form_id = form_id
        self.location = "????"
        
        # SPECIAL STATS
        self.strength = special[0]
        self.perception = special[1]
        self.endurance = special[2]
        self.charisma = special[3]
        self.intelligence = special[4]
        self.agility = special[5]
        self.luck = special[6]

        # Limbs
        self.head = 100
        self.l_arm = 100
        self.r_arm = 100
        self.l_leg = 100
        self.r_leg = 100

        self.journal = []
        self.inventory = []
        self.money = 15
        
        for item in inventory:
            new_item = copy.deepcopy(item_list[item])
            self.inventory.append(new_item)
        
        self.equipped = {}
        for count, item in enumerate(self.inventory):
            if count < 2:
                if item.form_id[0] == "w":
                    self.equipped[0] = item  
                elif item.form_id[0] == "a":
                    self.equipped[1] = item

    def limb_check(self):
        return

    # Calculates for one limb only
    def limb_dam(self, limb, dam):
        current_limb = getattr(self, limb)
        setattr(self, limb, current_limb - dam)
    
    def interacted(self, dweller):
        pass

    def deflect_chance(self, target):
        # Chance of enemy dodging attack
        try:
            armour_class = 5
            if target.armour.armour_type == "medium":
                armour_class += 5
            elif target.armour.armour_type == "heavy":
                armour_class += 3
            else:
                armour_class += 8
        except:
            armour_class = 5
        
        if random.randint(1, 75) <= armour_class:
            # Will Hit
            return True
        else:
            # Deflected
            return False

    def attack(self, target, location):
        combat_logs = []
        deflected = self.deflect_chance(target)
        if deflected:
            combat_logs.append(target.name + " dodged your attack")
            return (deflected, combat_logs)
        else:
            # Some vars to init for later
            try:
                tar_def = target.armour.threshold
            except:
                tar_def = target.dt

            if location.lower() == "head":
                lm = 2
            else:
                lm = 1

            weapon_used = self.equipped[0]
            if weapon_used.attack_type == "melee":
                # Melee attack
                dam = weapon_used.damage + (self.strength * 0.5)
                dam_adj = (dam - tar_def) * lm
            else:
                # Ranged attack
                dam = weapon_used.damage
                dam_adj = (dam - tar_def) * lm
            # Should always be true, likely useless check here
            if dam_adj > 0:
                combat_logs.append("You hit {} for {} damage".format(target.name, str(dam_adj)))
                target.health -= dam_adj         
            
            # Check if they are destroyed
            destroyed = False
            if target.health <= 1:
                destroyed = True
                combat_logs.append("You have destroyed the " + target.name)

            return(deflected, combat_logs, destroyed)

    # Checks the validity of a a movement
    def move_choice(self, mdir, vault, object_list):
        # User wants to quit
        if mdir == "q":
            print(Fore.RED + 'Do you want to quit? (Y\\N)')
            key = getch()
            key = str(key)
            key=key.replace("b","")
            key=key.replace("'","")
            key=key.replace("'","")

            if key.lower() == "y":
                quit()
            else:
                return
        # Opened the inventory
        elif mdir == "i":
            print(Fore.GREEN + "Equipped")
            try:
                print(self.equipped[0].name)
            except:
                print("You have no weapon")
            try:
                print(self.equipped[1].name)
            except:
                print("You have no armour")
    
            print(Fore.GREEN + "Inventory")
            for count, item in enumerate(self.inventory):
                print(str(count) + ": " + item.name)
            a = input()
            try:
                # move item to equipped, weapon goes to first slot, armour to second
                a = int(a)
                item_to_add = self.inventory[a]

                if item_to_add.form_id[0] == "w":
                    self.equipped[0] = item_to_add
                
                elif item_to_add.form_id[0] == "a":
                    self.equipped[1] = item_to_add
                return
            except:
                print("You cant equip that.")
                a = input()
                return
        else:
            # Checks normal movement
            # up, down
            count = []
            if mdir == "w":
                # Not at the top or xpos exist for current and above 
                if self.ypos > 0:
                    for item in vault[self.ypos - 1]:
                        count.append(item.xpos)
                    if self.xpos in count:
                        if vault[self.ypos - 1][self.xpos].icon == " ":
                            return True
                        else:
                            return False
            elif mdir == "s":
                # Above bottom, xpos exist for current and below
                if self.ypos < len(vault) - 1:
                    for item in vault[self.ypos + 1]:
                        count.append(item.xpos)
                    if self.xpos in count:
                        if vault[self.ypos + 1][self.xpos].icon == " ":
                            return True
                        else:
                            return False
            # left, right
            elif mdir == "a":
                if self.xpos > 0:
                    if vault[self.ypos][self.xpos - 1].icon == " ":
                        return True
                    
            elif mdir == "d":
                if self.xpos < len(vault[self.ypos]) - 1:
                    if vault[self.ypos][self.xpos + 1].icon == " ":
                        return True
                    return False
    
    def __str__(self):
        return "Yourself"