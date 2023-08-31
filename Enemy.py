from Alive_Entity import *
from copy import copy
from Items import *

# the base enemy class
class Enemy(Alive_Entity):
    def __init__(self, name, health, attack, movement_speed, knockback, sprite):
        super().__init__(name, health, attack, movement_speed, knockback, sprite)
        self.holding = []
        self.move_in_random_dir_timer_max = 60*random.randrange(1,5)
        self.move_in_random_dir_timer = self.move_in_random_dir_timer_max

    def pick_random_dir(self):
        cur_dir = copy(self.moving_dir)
        start_dir = copy(self.moving_dir)

        while start_dir == cur_dir:
            rand_num = random.randrange(0,4)
            #print("Picking", cur_dir, rand_num)
            if rand_num == 0:
                start_dir = Direction.UP
            elif rand_num == 1:
                start_dir = Direction.DOWN
            elif rand_num == 2:
                start_dir = Direction.LEFT
            elif rand_num == 3:
                start_dir = Direction.RIGHT
        return start_dir

    def move_in_random_dir(self):
        self.set_moving_dir(self.pick_random_dir())
    
    def add_holding_item(self, item_class):
        #if isinstance(item_class, Item):
        item = item_class(0,0,self.sprite.coord, False)
        self.holding.append(item)

    def random_change_to_add_item(self, item_class, chance):
        holding = random.randrange(0,100)
        if holding < chance:
            self.add_holding_item(item_class)

    def drop_items(self):
        return self.holding

    def reset_move_in_random_dir_timer(self):
        self.move_in_random_dir_timer = self.move_in_random_dir_timer_max

    def draw(self):
        self.sprite.draw()
        if self.move_in_random_dir_timer <= 0:
            self.move_in_random_dir()
            self.reset_move_in_random_dir_timer()
        self.move_in_random_dir_timer -= 1

class Slime(Enemy):
    def __init__(self, i, j):
        self.main_sprite = pygame.image.load("./sprites/slime.png")
        sprite = Sprite(
            4, # scale factor
            self.main_sprite,
            i, #i
            j, # j
            None,
            True,
            .5,
            .5
        )
        super().__init__(
            "Slime",
            30, # health
            1, # attack
            2, # movement speed
            0, # knockback
            sprite)
        
        self.move_in_random_dir()
        #self.add_holding_item(Key)

class Bat(Enemy):
    def __init__(self, i, j):
        self.main_sprite = pygame.image.load("./sprites/bat.png")
        sprite = Sprite(
            4, # scale factor
            self.main_sprite,
            i, #i
            j, # j
            None,
            True,
            .5,
            .5
        )
        super().__init__(
            "Slime",
            4, # health
            4, # attack
            2, # movement speed
            0,
            sprite)
        
        self.move_in_random_dir()
        #self.add_holding_item(Key)

    

class Skeleton(Enemy):
    # a simple enemy 
    # coord is the starting position of the skeleton, is_hor_moving is a bool which determines whether the skeleton patrols hor or vertically 
    def __init__(self, i, j, is_hor_moving):
        self.down_sprite = pygame.image.load("./sprites/skeleton_sprites/tile007.png")
        self.up_sprite = pygame.image.load("./sprites/skeleton_sprites/tile001.png")
        self.left_sprite = pygame.image.load("./sprites/skeleton_sprites/tile011.png")
        self.right_sprite = pygame.image.load("./sprites/skeleton_sprites/tile005.png")
        
        sprite = Sprite(
            1.5, # scale factor
            self.down_sprite,
            i, #i
            j, # j
            None,
            True,
            .7,
            .7
        )
        super().__init__(
            "Skeleton", 
            6 , # health
            2, # attack
            1, # movement speed
            0, # knockback
            sprite)  

        self.start_pos = get_middle_coord(i,j)
        #copy(coord)#copy(self.hitbox.center)
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

        # held items
        self.random_change_to_add_item(Heart, 25)
        

    def update_sprite(self):
        if self.moving_dir == Direction.DOWN:
            self.sprite.set_new_sprite(self.down_sprite)
        elif self.moving_dir == Direction.UP:
            self.sprite.set_new_sprite(self.up_sprite)
        elif self.moving_dir == Direction.LEFT:
            self.sprite.set_new_sprite(self.left_sprite)
        elif self.moving_dir == Direction.RIGHT:
            self.sprite.set_new_sprite(self.right_sprite)
        else:
            self.sprite.set_new_sprite(self.down_sprite)

    def draw(self):
        self.update_sprite()
        self.sprite.draw()
        self.draw_waypoints()
        #pygame.draw.circle(screen, red, self.hitbox.center, 2)

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
        cur_pos = self.sprite.hitbox.center
        
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
