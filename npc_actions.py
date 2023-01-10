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
        self.inventory = holder[6]
        self.form_id = holder[7]
        self.hp = holder[8]
        self.weapon = holder[9]

    def set_pos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos

    def interacted(self, dweller):
        # intro
        print(Fore.GREEN + "You are interacting with " +  self.name)
        print(Fore.GREEN + "You can do the following:")
        for each in self.avail_options:
            print(each)
        
        # user input
        # each option should be checker here as will break otherwise
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
        dweller.inventory.append("apple")

    def trade(self, dweller):
        print(Fore.BLUE + "See my wares!")
        for item in self.inventory:
            print("{} : {}".format(item, self.inventory[item]))
        print("Please choose one:")
        to_choose = input()
        if to_choose in self.inventory:
            if dweller.money >= self.inventory[to_choose]:
                dweller.money -= self.inventory[to_choose]
                dweller.inventory.append(to_choose)
                print(Fore.GREEN + "Thank you for your business!")
            else:
                print(Fore.RED + "Sorry, but you dont have the coin!")
        else:
            print(Fore.RED + "That item isn't in my inventory, please try again")

# always hostile, built for fighting, along with few other systems
class Enemy(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.health = holder[1]
        self.damage = holder[2]
        self.rad_damage = holder[3]
        self.sight = holder[4]
        self.inventory = holder[5]
        self.form_id = holder[6]