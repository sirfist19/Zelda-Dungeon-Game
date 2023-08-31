from fund_values import *

# this is the base class of all objects
# it is pretty much just used to draw stuff

# also has some simple movement stuff
class Sprite:
    def __init__(self, scale_factor, cur_sprite, i, j, coord, using_ij, hor_mult, vert_mult) -> None:
        self.scale_factor = scale_factor
        self.cur_sprite = cur_sprite
        self.cur_sprite = self.scale_sprite()
        self.hor_mult = hor_mult
        self.vert_mult = vert_mult
        if using_ij:
            self.set_sprite_ij(i,j)
        else:
            self.set_sprite_coord(coord)
        self.hitbox = self.get_hitbox()

    # continuous movement of a sprite with some direction and speed
    def move(self, dir, speed): 
        if dir == Direction.UP:
            self.coord[1] -= speed
        elif dir == Direction.DOWN:
            self.coord[1] += speed
        elif dir == Direction.LEFT:
            self.coord[0] -= speed
        elif dir == Direction.RIGHT:
            self.coord[0] += speed
        print(self.coord)
        
    def set_sprite_coord(self, coord):
        self.coord = coord

    def set_sprite_ij(self, i, j):
        self.coord = self.center_sprite_at_coord(i, j)
    
    def get_sprite_ij(self):
        # convert the coord to i and j
        return get_ij_from_coord(self.coord)
    
    # def tile_push(self, dir):
    #   push sprite over a tile

    def center_sprite_at_coord(self, i, j):
        #middle = get_top_left_coord(i, j)
        middle = get_middle_coord(i, j)
        #print(f"Sprite width: {self.cur_sprite.get_width()}")
        return [middle[0] -  (self.cur_sprite.get_width()/2), 
                middle[1] - (self.cur_sprite.get_height()/2)]

    def scale_sprite(self):
        return pygame.transform.scale(self.cur_sprite, 
                                      (self.cur_sprite.get_width() * self.scale_factor, 
                                       self.cur_sprite.get_height() * self.scale_factor))
                
    def set_new_sprite(self, new_sprite_img):
        self.cur_sprite = new_sprite_img
        self.cur_sprite = self.scale_sprite()
    
    def get_sprite_center(self):
        return [self.coord[0] + self.cur_sprite.get_width()/2,
                self.coord[1] + self.cur_sprite.get_height()/2]
    
    def get_hitbox(self):
        center = self.get_sprite_center()
        top_left_x = center[0] - self.hor_mult*self.cur_sprite.get_width()/2
        top_left_y = center[1] - self.vert_mult*self.cur_sprite.get_height()/2
        bottom_right_x = self.hor_mult*self.cur_sprite.get_width()
        bottom_right_y = self.vert_mult*self.cur_sprite.get_height()
        return pygame.Rect(
            top_left_x,
            top_left_y,
            bottom_right_x,
            bottom_right_y
        )
        return pygame.Rect(self.coord[0], 
                           self.coord[1],
                           self.hor_mult*self.cur_sprite.get_width(),
                           self.vert_mult*self.cur_sprite.get_height())
        
    
    def draw(self):
        #scaled_cur_sprite = self.scale_sprite()
        
        screen.blit(self.cur_sprite, self.coord)
        
        #print(cur_sprite.get_width(), cur_sprite.get_height())
        # Assuming you have a character object with x, y, width, and height properties
        self.draw_hitbox()
        #pygame.draw.circle(screen, black, self.coord, 3)
        
    
    def draw_center(self):
        pygame.draw.circle(screen, red, self.get_sprite_center(), 3)
        
    def draw_hitbox(self):
        self.hitbox = self.get_hitbox()
        
        if DRAW_HIT_BOXES:
            pygame.draw.rect(screen, white, self.hitbox, 2)
            self.draw_center()
