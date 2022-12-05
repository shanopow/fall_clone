from getch import getch
class Player(object):
    def __init__(self, name, health, xp, rads, xpos, ypos, icon, form_id):
        # Basic
        self.name = name
        self.health = health
        self.xp = xp
        self.rads = rads
        self.xpos = xpos
        self.ypos = ypos
        self.icon = icon
        self.form_id = form_id
        # Limbs
        self.head = 100
        self.l_arm = 100
        self.r_arm = 100
        self.l_leg = 100
        self.r_leg = 100

        self.inventory = []
        self.money = 5

    def limb_check(self):
        return

    # Calculates for one limb only
    def limb_dam(self, limb, dam):
        current_limb = getattr(self, limb)
        setattr(self, limb, current_limb - dam)
        
    def move_choice(self, mdir, vault):
        # user wants to quit
        if mdir == "q":
            print('Do you want to quit? (Y\\N)')
            key = getch()
            key = str(key)
            key=key.replace("b","")
            key=key.replace("'","")
            key=key.replace("'","")

            if key.lower() == "y":
                quit()
            else:
                return
        else:
            # up, down
            count = []
            if mdir == "w":
                # Not at the top or xpos exist for current and above 
                if self.ypos > 0:
                    for item in vault[self.ypos - 1]:
                        count.append(item.xpos)
                    if self.xpos in count:
                        return True
            elif mdir == "s":
                # Above bottom, xpos exist for current and below
                if self.ypos < len(vault) - 1:
                    for item in vault[self.ypos + 1]:
                        count.append(item.xpos)
                    if self.xpos in count:
                        return True
            # left, right
            elif mdir == "a":
                if self.xpos > 0:
                    return True
            elif mdir == "d":
                if self.xpos < len(vault[self.ypos]) - 1:
                    return True
            return False

    def over_item(self):
        return