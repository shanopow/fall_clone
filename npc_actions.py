from map_builder import move_calc

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

    # way this works is we check dir we want to move enemy through comparing ypos and xpos. Prefer to move across over down first.
    # Find horizontal and vertical dist between player and enemy first
    def movement(self, dweller, vault):
        # Find distance
        horiz_dist = dweller.xpos - self.xpos
        if horiz_dist < 0:
            horiz_dist = horiz_dist * -1
        vert_dist = dweller.ypos - self.ypos
        if vert_dist < 0:
            vert_dist = vert_dist * -1     
        
        # On dead straight line with Player
        # Also includes choosing to attack
        if self.xpos == dweller.xpos:
            # Check the areas above and below for a player
            if self.ypos == dweller.ypos - 1 or self.ypos == dweller.ypos + 1:
                self.interacted(dweller)
            
            # Vertical
            # Try to move down
            elif self.ypos < dweller.ypos and vault[self.ypos - 1][self.xpos].icon == " ":
                vault = move_calc(vault, self, self.xpos, self.ypos + 1)

            # Try to move up
            elif self.ypos > dweller.ypos and vault[self.ypos + 1][self.xpos].icon == " ": 
                vault = move_calc(vault, self, self.xpos, self.ypos - 1)
        
        elif self.ypos == dweller.ypos: 
            if self.xpos == dweller.xpos - 1 or self.xpos == dweller.xpos + 1:
                self.interacted(dweller)
            
            # Hoizontal
            # Try to move to the Right
            elif self.xpos < dweller.xpos and vault[self.ypos][self.xpos + 1].icon == " ":
                vault = move_calc(vault, self, self.xpos + 1, self.ypos)

            # Try to move to the Left
            elif self.xpos > dweller.xpos and vault[self.ypos][self.xpos - 1].icon == " ":
                vault = move_calc(vault, self, self.xpos - 1, self.ypos + 1)

        # Weirder movement
        elif horiz_dist <= vert_dist:
            # Horizontal
            # Try to move to the Right
            if self.xpos < dweller.xpos and vault[self.ypos][self.xpos + 1].icon == " ":
                vault = move_calc(vault, self, self.xpos + 1, self.ypos)

            # Try to move to the Left
            elif self.xpos > dweller.xpos and vault[self.ypos][self.xpos - 1].icon == " ":
                vault = move_calc(vault, self, self.xpos - 1, self.ypos)

        elif vert_dist < horiz_dist:
            # Vertical
            # Try to move down
            if self.ypos < dweller.ypos and vault[self.ypos - 1][self.xpos].icon == " ":
                vault = move_calc(vault, self, self.xpos, self.ypos + 1)

            # Try to move up
            if self.ypos > dweller.ypos and vault[self.ypos + 1][self.xpos].icon == " ": 
                vault = move_calc(vault, self, self.xpos, self.ypos - 1)

        self.moved = True
        return vault

    def __str__(self):
        return self.name
    
    def hit_chance(self, dweller):
        # chance of enemy dodging attack
        armour_class = dwller.agility
        if dweller.equipped[1].armour_type == "medium":
            armour_class += 5
        elif dweller.equipped[1].armour_type == "heavy":
            armour_class += 3
        else:
            armour_class += 8
        
        if random.randint(1, 75) <= armour_class:
            # Will Hit
            return True
        else:
            # Deflected
            return False


class Animal(Enemy):
    def __init__(self, holder):
        super().__init__(holder)
        self.damage = holder[5]
        self.dt = holder[6]
        self.animal_style = holder[7]


    
    def interacted(self, dweller):
        print("working")
        quit()
    
    # Animals just use their basic attack stat, compared simply to player dt    
    def attack(self, dweller):
        # chance to hit, fasle if player dodges
        go_ahead = self.hit_chance(dweller)
        if go_ahead:
            labone = True     
        else:
            return(self.name, "missed you completely!")

class Hostile(Enemy):
    def __init__(self, holder):
        super().__init__(holder)
        self.weapon = holder[5]
        self.armour = holder[6]

    
    def interacted(self, dweller):
        print("working")
        quit()

    # Hostiles will use their weapon to attack enemy, weapon attack is compared to player dt
    def attack(self):
        # chance to hit, false if payer dodges
        go_ahead = self.hit_chance(dweller)
        if go_ahead:
            # important
            labone = True
        else:
            return(self.name, "missed you completely!")