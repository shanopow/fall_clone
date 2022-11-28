class Npc(object):
    def __init__(self, name, xpos, ypos, has_dialogue, status, icon, id, dialogue=["I have no interesting dialogue", "Goodbye!"]):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.has_dialogue = has_dialogue
        self.status = status
        self.icon = icon
        self.id = id
        self.dialogue = dialogue

    def interacted(self, interaction_type):
        if interaction_type == "talk":
            for item in self.dialogue:
                print(item)
            a = input()