from colorama import init, Fore, Back, Style
init(autoreset=True)

class Npc(object):
    def __init__(self, holder):
        self.name = holder[0]
        self.xpos = holder[1]
        self.ypos = holder[2]
        if holder[3] == "1":
            self.aggression = True
        else:
            self.aggression = False

        self.npc_type = holder[4]
        self.icon = holder[5]
        self.dialogue = holder[6]
        self.npc_type = holder[7]
        self.inventory = holder[8]
        self.form_id = holder[9]

    def interacted(self, dweller):
        print("You are interacting with", self.name)
        print("Use talk, steal, etc")
        if self.npc_type == "trader":
            print(Fore.GREEN + "You can also trade with this person")
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