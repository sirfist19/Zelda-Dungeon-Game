from Alive_Entity import *

class Sword:
    def __init__(self):
        self.attack = 3
        self.width = 40
        self.height = 10
        self.offset = 10
        self.rect = pygame.Rect(0,0,0,0) # default rect

    def draw(self, hit_box, facing_dir, prev_facing_dir): 
        # the hit box can be either the player or enemies' hitbox
        #print("Drawing sword")
        center_x, center_y = hit_box.center
        hor_offset = hit_box.width / 2
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
        super().__init__("Link", 5 , 0, 5, [WIDTH/2,HEIGHT/2])
        # name, health, attack, movement_speed, coord
        self.idle_sprite = pygame.image.load("./sprites/knight_sprites/tile024.png")
        self.cur_sprite = pygame.image.load("./sprites/knight_sprites/tile024.png")
        self.scale_factor = 3
        self.hitbox = pygame.Rect(0,0,20,20) # a default starting rect

        # for sword
        self.sword = Sword()
        self.is_attacking = False

    def update_sprite(self):
        #if self.moving_dir == Direction.DOWN:
        self.cur_sprite = self.idle_sprite

    def attacking(self):
        if self.is_attacking:
            self.sword.draw(self.hitbox, self.moving_dir, self.prev_moving_dir)
            
    def draw(self):
        self.update_sprite()

        self.cur_sprite = pygame.transform.scale(self.cur_sprite, (self.cur_sprite.get_width() * self.scale_factor,
                                                      self.cur_sprite.get_height() * self.scale_factor))
        screen.blit(self.cur_sprite, self.coord)
        #print(cur_sprite.get_width(), cur_sprite.get_height())
        # Assuming you have a character object with x, y, width, and height properties
        self.draw_hitbox()
        #self.draw_center()
        self.attacking()
        #hor_mult = .5
        #vert_mult = .6
        #self.hitbox = pygame.Rect(self.coord[0] + cur_sprite.get_width()/4, self.coord[1] + cur_sprite.get_height()/4, hor_mult*cur_sprite.get_width(), vert_mult*cur_sprite.get_height())
        #hitbox = pygame.Rect(self.coord[0] , self.coord[1] , .75*cur_sprite.get_width(), .75*cur_sprite.get_height())
        
        #pygame.draw.rect(screen, white, self.hitbox, 2)  # Red rectangle with 2-pixel width
    
    def draw_center(self):
        pygame.draw.circle(screen, red, self.hitbox.center, 3)
        
    def draw_hitbox(self):
        hor_mult = .5
        vert_mult = .6
        self.hitbox = pygame.Rect(self.coord[0] + self.cur_sprite.get_width()/4, self.coord[1] + self.cur_sprite.get_height()/4, hor_mult*self.cur_sprite.get_width(), vert_mult*self.cur_sprite.get_height())
        
        if DRAW_HIT_BOXES:
            pygame.draw.rect(screen, white, self.hitbox, 2)

    def spawn_at_south_door(self):
        self.coord = get_top_left_coord(NUM_TILES_WIDE//2 - .25, NUM_TILES_TALL-3.5)
    def spawn_at_north_door(self):
        self.coord = get_top_left_coord(NUM_TILES_WIDE//2 - .25, 1.7)
    def spawn_at_west_door(self):
        self.coord = get_top_left_coord(2, NUM_TILES_TALL/2 - 1)
    def spawn_at_east_door(self):
        self.coord = get_top_left_coord(NUM_TILES_WIDE-3.5, NUM_TILES_TALL/2 - 1)
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
