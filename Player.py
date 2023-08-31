from Alive_Entity import *
import math

class Sword:
    def __init__(self):
        self.attack = 3
        self.width = 40
        self.height = 10
        self.offset = 10
        self.rect = None # default rect
    
    def reset_sword(self):
        self.rect = None

    def draw(self, hit_box, facing_dir, prev_facing_dir): 
        # the hit box can be either the player or enemies' hitbox
        #print("Drawing sword")
        center_x, center_y = hit_box.center
        hor_offset = hit_box.width / 3#2
        vert_offset = hit_box.height/2

        if facing_dir == Direction.UP or (facing_dir == Direction.NOT_MOVING and prev_facing_dir == Direction.UP):
            sword_x = center_x 
            sword_y = center_y - vert_offset - self.width
            self.rect = pygame.Rect(sword_x, sword_y, self.height, self.width)
        elif facing_dir == Direction.DOWN or (facing_dir == Direction.NOT_MOVING and prev_facing_dir == Direction.DOWN):
            sword_x = center_x 
            sword_y = center_y + vert_offset
            self.rect = pygame.Rect(sword_x, sword_y, self.height, self.width)
        elif facing_dir == Direction.LEFT or (facing_dir == Direction.NOT_MOVING and prev_facing_dir == Direction.LEFT):
            sword_x = center_x - hor_offset - self.width
            sword_y = center_y
            self.rect = pygame.Rect(sword_x, sword_y, self.width, self.height)
        elif facing_dir == Direction.RIGHT \
            or (facing_dir == Direction.NOT_MOVING and prev_facing_dir == Direction.RIGHT) \
            or (facing_dir == Direction.NOT_MOVING and prev_facing_dir == Direction.NOT_MOVING):
            sword_x = center_x + hor_offset
            sword_y = center_y
            self.rect = pygame.Rect(sword_x, sword_y, self.width, self.height)

        pygame.draw.rect(screen, green, self.rect)
        #pygame.draw.circle(screen, red, (center_x, center_y), 5)

class Player(Alive_Entity):
    def __init__(self):
        # player specific input
        self.e_pressed = False

        # sounds
        self.player_hurt_sound = pygame.mixer.Sound("./sounds/player_hurt.mp3")

        # name, health, attack, movement_speed, coord
        self.idle_sprite = pygame.image.load("./sprites/knight_sprites/tile024.png")
        self.right_sprite = pygame.image.load("./sprites/knight_sprites/tile024.png")
        self.right_sprite_red = pygame.image.load("./sprites/knight_sprites/player_right_damage.png")
        self.has_damaged_sprite = False
        self.damage_sprite_timer_max = IFRAME_TIME
        self.damage_sprite_timer = self.damage_sprite_timer_max

        # for sword
        self.sword = Sword()
        self.attack_timer_max = IFRAME_TIME
        self.attack_timer = copy(self.attack_timer_max)
        self.is_attacking = False

        # keys
        self.keys = 0

        # gold
        self.gold = 0

        self.respawn_room_coord = [0,0]

        scale_factor = 3
        sprite = Sprite(scale_factor, 
                        self.right_sprite, 
                        8, # i
                        8, # j
                        [WIDTH/2,HEIGHT/2], # start coord
                        True, # using i and j
                        .5, # hor mult
                        .5) # vert mult
        
        super().__init__(
            "Link", # name
            50 , # health
            0, # attack
            5, # movement speed
            50, # knockback const
            sprite) 

    def update_sprite(self):
        #if self.moving_dir == Direction.DOWN:
        #self.cur_sprite = self.idle_sprite
        #self.sprite.set_new_sprite(self.idle_sprite)
       
        if self.has_damaged_sprite:
            print("Decreasing")
            self.damage_sprite_timer -= 1
        if self.damage_sprite_timer <= 0:
            self.damage_sprite_timer = self.damage_sprite_timer_max
            self.sprite.set_new_sprite(self.idle_sprite)
            self.has_damaged_sprite = False

    def attacking(self):
        # if the player is not pressing Enter then reset the attack_timer
        if not self.is_attacking:
            self.attack_timer = self.attack_timer_max
            self.sword.reset_sword()
        if self.attack_timer <= 0:
            self.sword.reset_sword()

        # if the player is pressing Enter and the timer is not 0, draw the sword
        if self.is_attacking and self.attack_timer > 0:
            #print("Drawing the sword")
            self.sword.draw(self.sprite.hitbox, self.moving_dir, self.prev_moving_dir)
            self.attack_timer -= 1
        #(self.attack_timer)

    def damage(self, amt):
        super().damage(amt)
        self.sprite.set_new_sprite(self.right_sprite_red)
        self.has_damaged_sprite = True

        # add some knockback to the player
        self.apply_knockback()

        # play the damage sound
        self.player_hurt_sound.play()

        

    def has_keys(self):
        return self.keys > 0
    
    def draw(self):
        self.update_sprite()
        self.sprite.draw()
        self.attacking()
    
    def spawn_at_south_door(self):
        self.sprite.set_sprite_coord(get_top_left_coord(NUM_TILES_WIDE//2 - .25, NUM_TILES_TALL-3.5))
        self.respawn_room_coord = copy(self.sprite.coord)

    def spawn_at_north_door(self):
        self.sprite.set_sprite_coord(get_top_left_coord(NUM_TILES_WIDE//2 - .25, 1.7))
        self.respawn_room_coord = copy(self.sprite.coord)

    def spawn_at_west_door(self):
        self.sprite.set_sprite_coord(get_top_left_coord(2, NUM_TILES_TALL/2 - 1))
        self.respawn_room_coord = copy(self.sprite.coord)

    def spawn_at_east_door(self):
        self.sprite.set_sprite_coord(get_top_left_coord(NUM_TILES_WIDE-3.5, NUM_TILES_TALL/2 - 1))
        self.respawn_room_coord = copy(self.sprite.coord)

    def spawn_at_respawn_room_coord(self):
        print(self.respawn_room_coord)
        self.sprite.set_sprite_coord(copy(self.respawn_room_coord))
'''
#screen.blit(decor_spritesheet, (WIDTH/2, HEIGHT/2))
SPRITE_WIDTH = 24

# make a surface to draw individual images on
image_surf = pygame.Surface((SPRITE_WIDTH, SPRITE_WIDTH)).convert_alpha() # convert alpha is to optimize pic quality in png
    
# blit the image you want on the image surface, 2nd param is place to blit on the new surface (image_surf) 
#   and 3rd is area including two coords of the top left corner to bottom right corner of the image from the spritesheet
image_surf.blit(decor_spritesheet, (0, 0), (0, 0, SPRITE_WIDTH, SPRITE_WIDTH))
    
# scale the image up
scale_factor = 3
image_surf = pygame.transform.scale(image_surf, (SPRITE_WIDTH * scale_factor, SPRITE_WIDTH * scale_factor))

# display the image surface
screen.blit(image_surf, (WIDTH/2, HEIGHT/2))
'''
