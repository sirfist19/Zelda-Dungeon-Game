from fund_values import *
from Sprite import Sprite

class Item:
    def __init__(self, sprite, i ,j):
        self.sprite = sprite
        self.i = i
        self.j = j

    def draw(self):
        self.sprite.draw()

    def get_rect(self): # gets the hitbox
        self.sprite.get_hitbox()

class Key(Item):
    def __init__(self, i, j, coord, usingij):
        scale_factor = 2
        cur_sprite = pygame.image.load("./sprites/key.png")
        sprite = Sprite(scale_factor, 
                        cur_sprite, 
                        i, 
                        j, 
                        coord, 
                        usingij, # using i j
                        .5, # hor mult
                        .7) # vert mult
        super().__init__(sprite, i, j)

class Heart(Item):
    def __init__(self, i, j, coord, usingij):
        scale_factor = 2
        self.heal_amt = 2
        cur_sprite = pygame.image.load("./sprites/heart.png")
        sprite = Sprite(scale_factor, 
                        cur_sprite, 
                        i, 
                        j, 
                        coord, 
                        usingij, # using i j
                        .5, # hor mult
                        .5) # vert mult
        super().__init__(sprite, i, j)

class Chest(Item):
    def __init__(self, i, j, coord, usingij, contained_item): 
        self.scale_factor = 3
        self.closed_img = pygame.image.load("./sprites/chest.png")
        self.closed_selected_img = pygame.image.load("./sprites/chest_selected.png")
        self.open_img =  pygame.image.load("./sprites/open_chest.png")
        self.opening_sound = pygame.mixer.Sound("./sounds/chest_open.mp3")

        sprite = Sprite(self.scale_factor, 
                        self.closed_img, 
                        i, 
                        j, 
                        coord, 
                        usingij, # using i j
                        .8, # hor mult
                        .85) # vert mult
        super().__init__(sprite, i, j)
        self.is_open = False
        self.contained_item = contained_item

    def open(self, player):
        # if the player is directly below the chest and pressing e, open the chest
        i, j = player.sprite.get_sprite_ij()
        player_at_opening_pos = i+1 == self.i and j == self.j
        
        #print(i, j, self.i, self.j, player.e_pressed)
        if not self.is_open and player_at_opening_pos:
            self.sprite.set_new_sprite(self.closed_selected_img)
        elif not self.is_open:
            self.sprite.set_new_sprite(self.closed_img)

        if not self.is_open and player_at_opening_pos and player.e_pressed: # if the player is directly below the chest
            self.is_open = True
            self.sprite.set_new_sprite(self.open_img)
            print("Opening chest")
            self.opening_sound.play()
            # return the held item
            return self.contained_item(i, j+1, None, True)
            

class Gold(Item):
    def __init__(self, i, j, coord, usingij): 
        scale_factor = 3
        cur_sprite = pygame.image.load("./sprites/gold.png")
        sprite = Sprite(scale_factor, 
                        cur_sprite, 
                        i, 
                        j, 
                        coord, 
                        usingij, # using i j
                        .8, # hor mult
                        .85) # vert mult
        super().__init__(sprite, i, j)
        