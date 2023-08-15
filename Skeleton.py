from Alive_Entity import *
from copy import copy

class Skeleton(Alive_Entity):
    # a simple enemy 
    # coord is the starting position of the skeleton, is_hor_moving is a bool which determines whether the skeleton patrols hor or vertically 
    def __init__(self, coord, is_hor_moving):

        super().__init__("Skeleton", 3 , 1, 1, coord) # name, health, attack, movement_speed, coord, moving_dir
        self.down_sprite = pygame.image.load("./sprites/skeleton_sprites/tile007.png")
        self.up_sprite = pygame.image.load("./sprites/skeleton_sprites/tile001.png")
        self.left_sprite = pygame.image.load("./sprites/skeleton_sprites/tile011.png")
        self.right_sprite = pygame.image.load("./sprites/skeleton_sprites/tile005.png")
        self.scale_factor = 1.5
        self.cur_sprite = self.get_cur_sprite()
        self.hitbox = self.get_hitbox()
        self.start_pos = copy(coord)#copy(self.hitbox.center)
        self.is_hor_moving = is_hor_moving
        self.patrol_length = 3*TILE_WIDTH
        
        if is_hor_moving:
            self.set_moving_dir(Direction.RIGHT)
            self.end_pos = [self.start_pos[0] + self.patrol_length, self.start_pos[1]]
        else:
            self.set_moving_dir(Direction.DOWN)
            self.end_pos = [self.start_pos[0], self.start_pos[1] + self.patrol_length]
        self.waypoint_width = 5
        self.width = 30

    def update_sprite(self):
        if self.moving_dir == Direction.DOWN:
            self.cur_sprite = self.down_sprite
        elif self.moving_dir == Direction.UP:
            self.cur_sprite = self.up_sprite
        elif self.moving_dir == Direction.LEFT:
            self.cur_sprite = self.left_sprite
        elif self.moving_dir == Direction.RIGHT:
            self.cur_sprite = self.right_sprite
        else:
            self.cur_sprite = self.down_sprite

    def get_cur_sprite(self):
        self.update_sprite()
        return pygame.transform.scale(self.cur_sprite, (self.cur_sprite.get_width() * self.scale_factor,
                                                      self.cur_sprite.get_height() * self.scale_factor))
    def get_hitbox(self):
        hor_mult = .7
        vert_mult = .7
        return pygame.Rect(self.coord[0] + self.cur_sprite.get_width()/4, self.coord[1] + self.cur_sprite.get_height()/4, hor_mult*self.cur_sprite.get_width(), vert_mult*self.cur_sprite.get_height())
        
    def draw(self):
        self.cur_sprite = self.get_cur_sprite()
        
        screen.blit(self.cur_sprite, self.coord)
        self.draw_hitbox()
        self.draw_waypoints()
        pygame.draw.circle(screen, red, self.hitbox.center, 2)

    def draw_hitbox(self):
        self.hitbox = self.get_hitbox()
        if DRAW_HIT_BOXES:
            pygame.draw.rect(screen, white, self.hitbox, 2)

    def draw_waypoints(self):
        if DRAW_WAYPOINTS:
            self.draw_waypoint(self.start_pos)
            self.draw_waypoint(self.end_pos)
            
    def draw_waypoint(self, pos):
        pygame.draw.rect(
            screen, 
            white, 
            (pos[0], #+ #self.width/2, 
             pos[1], #+ #self.width/2, 
             self.waypoint_width, 
             self.waypoint_width)
        )

    def patrol(self):
        #print(f"Cur pos: {self.hitbox.center}, Start: {self.start_pos}, End: {self.end_pos}")
        cur_pos = self.hitbox.center
        
        if self.moving_dir == Direction.RIGHT and cur_pos[0] > self.end_pos[0]: # 
            self.set_opposite_dir()
        if self.moving_dir == Direction.LEFT and cur_pos[0] < self.start_pos[0]:
            self.set_opposite_dir()

        if self.moving_dir == Direction.DOWN and cur_pos[1] > self.end_pos[1]:
            self.set_opposite_dir()
        if self.moving_dir == Direction.UP and cur_pos[1] < self.start_pos[1]:
            self.set_opposite_dir()
        #print(self.moving_dir)
        '''
        if self.coord[0] >= self.end_pos[0]:
            self.set_moving_dir(Direction.LEFT)
        elif self.coord[0] <= self.start_pos[0]:
            self.set_moving_dir(Direction.RIGHT)
        elif self.coord[1] > self.end_pos[1]:
            self.set_moving_dir(Direction.UP)
        elif self.coord[1] < self.start_pos[1]:
            self.set_moving_dir(Direction.DOWN)
        '''
