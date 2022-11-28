from colorama import init, Fore, Back, Style
init(autoreset=True)

class Npc(object):
    def __init__(self, name, xpos, ypos, has_dialogue, aggression, icon, id, dialogue=["I have no interesting dialogue", "Goodbye!"], npc_type="generic", inventory = None):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.has_dialogue = has_dialogue
        self.aggression = aggression
        self.icon = icon
        self.id = id
        self.dialogue = dialogue
        self.npc_type = npc_type
        if inventory != None:
            self.inventory = inventory
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
            dweller.inv.append("apple")
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
            print(Fore.RED + "That item isn't in my inventory, sorry!")