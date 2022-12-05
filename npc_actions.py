from colorama import init, Fore, Back, Style
init(autoreset=True)

class Npc(object):
    def __init__(holder):
        self.name = holder[0]
        self.xpos = holder[1]
            self.ypos = holder[2]
        self.aggression = holder[3]
        self.icon = holder[4]
        self.npc_type = holder[5]
        
        if self.dialogue != " ":
            self.dialogue = holder[6]
        else:
            self.dialogue = []
        
        if inventory != " ":
            self.inventory = holder[8]
        else:
            self.inventory = []

    def interacted(self, dweller):
        print("You are interacting with", self.name)
        print("Use talk, steal, etc")
        if self.npc_type == "trader":
            print(Fore.GREEN + "You can also trade with this person")
        interaction_type = input()
        interaction_type = interaction_type.lower() 
        if interaction_type == "talk":
            for item in self.dialogue:
                print(item)
            a = input()
        elif interaction_type == "steal":
            # This will be percentage based in future
            print("Success!")
            print("You stole an apple!")
            dweller.inventory.append("apple")
            a = input()
        elif interaction_type == "trade" and self.npc_type == "trader":
            print(Fore.BLUE + "See my wares!")
            self.transaction(dweller)
            a = input()
    
    def transaction(self, dweller):
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