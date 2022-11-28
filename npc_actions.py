class Npc(object):
    def __init__(self, name, xpos, ypos, has_dialogue, aggression, icon, id, dialogue=["I have no interesting dialogue", "Goodbye!"]):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.has_dialogue = has_dialogue
        self.aggression = aggression
        self.icon = icon
        self.id = id
        self.dialogue = dialogue

    def interacted(self, dweller):
        print("You are interacting with", self.name)
        print("Use talk, etc")
        interaction_type = input() 
        if interaction_type == "talk":
            for item in self.dialogue:
                print(item)
            a = input()