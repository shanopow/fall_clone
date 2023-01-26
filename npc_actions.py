# File Imports
from map_builder import move_calc, combat_manager

# Module Imports
from random import randint
from colorama import init, Fore, Back, Style
init(autoreset=True)

class Npc(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.avail_options = holder[1]
        self.can_fight = holder[2]
        self.icon = holder[3]
        self.dialogue = holder[4]
        self.npc_type = holder[5]
        self.trade_inventory = holder[6]
        self.form_id = holder[7]
        self.hp = holder[8]
        self.weapon = holder[9]
        self.inventory = holder[10]
        self.quest_dial = holder[11]

    def set_pos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
    
    def interacted(self, dweller):
        # Intro
        print(Fore.GREEN + "You are interacting with " +  self.name)
        print(Fore.GREEN + "You can do the following:")
        for each in self.avail_options:
            print(each)
        
        # User input
        # Each option should be checker here as will break otherwise
        interaction_type = input()
        interaction_type = interaction_type.lower() 
        if interaction_type == "talk":
            self.talk()
            a = input()
        
        elif interaction_type == "steal":
            self.steal(dweller)
            a = input()
        
        elif interaction_type == "trade" and self.npc_type == "trader":
            self.trade(dweller)
            a = input()

    def __str__(self):
        return self.name

    def talk(self):
        if self.dialogue == []:
            print("I have nothing to say to you")
        else:
            for item in self.dialogue:
                print(item)

    def steal(self, dweller):
        # This will be percentage based in future
        print("Success!")
        print("You stole an apple!")
        dweller.trade_inventory.append("apple")

    def trade(self, dweller):
        print(Fore.BLUE + "See my wares!")
        for item in self.trade_inventory:
            print("{} : {}".format(item, self.trade_inventory[item]))
        print("Please choose one:")
        to_choose = input()
        if to_choose in self.trade_inventory:
            if dweller.money >= self.trade_inventory[to_choose]:
                dweller.money -= self.trade_inventory[to_choose]
                dweller.inventory.append(to_choose)
                del self.trade_inventory[to_choose]
                print(Fore.GREEN + "Thank you for your business!")
            else:
                print(Fore.RED + "Sorry, but you dont have enough coins!")
        else:
            print(Fore.RED + "That item isn't in my inventory, please try again")

# Always hostile, built for fighting, along with few other systems
class Enemy(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.health = holder[1]
        self.drops = holder[2]
        self.form_id = holder[3]
        self.icon = holder[4]
        self.moved = False

    # Checks the validity of the move we want to make
    def move_valid(self, mdir, vault):
        # up, down
        count = []
        if mdir == "w":
            # Not at the top or xpos exist for current and above 
            if self.ypos > 0:
                for item in vault[self.ypos - 1]:
                    count.append(item.xpos)
                if self.xpos in count:
                    if vault[self.ypos - 1][self.xpos].item_at is None:
                        return True
                    else:
                        return False
        elif mdir == "s":
            # Above bottom, xpos exist for current and below
            if self.ypos < len(vault) - 1:
                for item in vault[self.ypos + 1]:
                    count.append(item.xpos)
                if self.xpos in count:
                    if vault[self.ypos + 1][self.xpos].item_at is None:
                        return True
                    else:
                        return False
        # left, right
        elif mdir == "a":
            if self.xpos > 0:
                if vault[self.ypos][self.xpos - 1].item_at is None:
                    return True
                
        elif mdir == "d":
            if self.xpos < len(vault[self.ypos]) - 1:
                if vault[self.ypos][self.xpos + 1].item_at is None:
                    return True
                return False
        return False
    # way this works is we check dir we want to move enemy through comparing ypos and xpos. Prefer to move across over down first.
    # Find horizontal and vertical dist between player and enemy first
    def movement(self, dweller, vault):
        # Find distance
        vert_dist = self.ypos - dweller.ypos
        horiz_dist = self.xpos - dweller.xpos
        if vert_dist < 0:
            vert_dist = vert_dist * -1
        if horiz_dist < 0:
            horiz_dist = horiz_dist * -1
        
        # On dead straight line with Player
        # Also includes choosing to attack
        can_w = self.move_valid("w", vault)
        can_a = self.move_valid("a", vault)
        can_s = self.move_valid("s", vault)
        can_d = self.move_valid("d", vault)

            
        if self.ypos == dweller.ypos: 
            # Hoizontal
            # Try to move to the right
            if can_d:
                vault = move_calc(vault, self, self.xpos + 1, self.ypos)

            # Try to move to the left
            elif can_a:
                vault = move_calc(vault, self, self.xpos - 1, self.ypos + 1)

        elif self.xpos == dweller.xpos:
            # Vertical
            # Try to move down
            if can_s:
                vault = move_calc(vault, self, self.xpos, self.ypos + 1)

            # Try to move up
            elif can_w:
                vault = move_calc(vault, self, self.xpos, self.ypos - 1)

        # Weirder movement
        elif horiz_dist >= vert_dist:
            # Horizontal
            # Try to move to the right
            if can_d:
                vault = move_calc(vault, self, self.xpos + 1, self.ypos)

            # Try to move to the left
            elif can_a:
                vault = move_calc(vault, self, self.xpos - 1, self.ypos)

        elif horiz_dist < vert_dist:
            # Vertical
            # Try to move down
            if can_s:
                vault = move_calc(vault, self, self.xpos, self.ypos + 1)

            # Try to move up
            elif can_w:
                vault = move_calc(vault, self, self.xpos, self.ypos - 1)

        self.moved = True
        return vault

    def deflect_chance(self, dweller):
        # chance of enemy dodging attack
        armour_class = dweller.agility
        if dweller.equipped[1].armour_type == "medium":
            armour_class += 5
        elif dweller.equipped[1].armour_type == "heavy":
            armour_class += 3
        else:
            armour_class += 8
        
        if randint(1, 75) <= armour_class:
            # Will Hit
            return True
        else:
            # Deflected
            return False

    def __str__(self):
        return self.name


class Animal(Enemy):
    def __init__(self, holder):
        super().__init__(holder)
        self.damage = holder[5]
        self.dt = holder[6]
        self.animal_style = holder[7]

    # Animals just use their basic attack stat, compared simply to player dt    
    def attack(self, target, location):
        combat_logs = []
        
        deflected = self.deflect_chance(target)
        if deflected:
            combat_logs.append("You managed to dodge the attack")
            return (deflected, combat_logs)
        
        else:
            # Some vars to init for later
            tar_def = target.equipped[1].threshold
            if location.lower() == "head":
                lm = 2
            else:
                lm = 1
            
            # Simple damage calculation
            dam_adj = (self.damage - tar_def) * lm
            
            # Should always be true, likely useless check here
            if dam_adj > 0:
                combat_logs.append("You hit {} for {} damage".format(target.name, str(dam_adj)))
                target.health -= dam_adj         

            # Check if they are destroyed
            destroyed = False
            if target.health <= 1:
                destroyed = True
                combat_logs.append("You have been destroyed by " + self.name)
            return(deflected, combat_logs, destroyed)

class Hostile(Enemy):
    def __init__(self, holder):
        super().__init__(holder)
        self.weapon = holder[5]
        self.armour = holder[6]
    
    # Hostiles will use their weapon to attack enemy, weapon attack is compared to player dt
    def attack(self, target, location):
        combat_logs = []
        
        deflected = self.deflect_chance(target)
        if deflected:
            combat_logs.append("You managed to dodge the attack")
            return (deflected, combat_logs)
        
        else:
            # Some vars to init for later
            tar_def = target.armour.threshold
            if location.lower() == "head":
                lm = 2
            else:
                lm = 1
            
            # Simple damage calculation
            dam_adj = (self.damage - tar_def) * lm
            
            # Should always be true, likely useless check here
            if dam_adj > 0:
                combat_logs.append("You hit {} for {} damage".format(target.name, str(dam_adj)))
                target.health -= dam_adj         

            # Check if they are destroyed
            destroyed = False
            if target.health <= 1:
                destroyed = True
                combat_logs.append("You have been destroyed by " + self.name)
            return(deflected, combat_logs, destroyed)
