from fund_values import *
from Sprite import Sprite

class Tile:
    def __init__(self):
        self.tile_scaling = 3.75
        self.sprite = None

    def draw(self, i, j):
        #print(self.symbol)
        self.sprite.set_sprite_ij(i,j)
        self.sprite.draw()

    def draw_rect(self, color, i, j): # i and j are the col and row respectively
        # the tilemap calls this method on the derived tiles and the derived tiles draw this method to draw all the tiles
        pygame.draw.rect(
                    screen,
                    color, 
                    pygame.Rect(i*TILE_WIDTH, j*TILE_WIDTH, TILE_WIDTH,TILE_WIDTH)
    )
    
    def set_sprite(self, img):
        self.sprite = Sprite(self.tile_scaling, img, 0, 0, None, True, 1, 1)

    def get_rect(self, i, j):
        return pygame.Rect(i*TILE_WIDTH, j*TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)

class Wall(Tile):
    def __init__(self, wall_dir=TileDirection.TOP):
        super().__init__()
        #self.top = pygame.image.load("./sprites/dungeon_tiles/wall_top.png")
        #self.bottom = pygame.image.load("./sprites/dungeon_tiles/wall_bottom.png")
        self.left = pygame.image.load("./sprites/my_dungeon_tiles/wall_left.png")
        self.right = pygame.image.load("./sprites/my_dungeon_tiles/wall_right.png")
        self.middle = pygame.image.load("./sprites/my_dungeon_tiles/wall_middle.png")
        self.full_left = pygame.image.load("./sprites/my_dungeon_tiles/full_wall_left.png")
        self.full_right = pygame.image.load("./sprites/my_dungeon_tiles/full_wall_right.png")
        self.top_left_corner = pygame.image.load("./sprites/my_dungeon_tiles/top_left_corner.png")
        self.top_right_corner = pygame.image.load("./sprites/my_dungeon_tiles/top_right_corner.png")
        self.torch_left = pygame.image.load("./sprites/my_dungeon_tiles/torch_wall_left.png")
        self.torch_right = pygame.image.load("./sprites/my_dungeon_tiles/torch_wall_right.png")

        #if wall_dir == TileDirection.TOP:
        #    self.cur_sprite = self.top
        #elif wall_dir == TileDirection.BOTTOM:
        #    self.cur_sprite = self.bottom
        self.cur_sprite = self.middle
        self.set_sprite(self.cur_sprite)
        
        self.color = light_gray
        self.symbol = 'W'

class Background(Tile):
    def __init__(self):
        super().__init__()
        self.color = black
        self.symbol = 'B'

    def draw(self, i, j):
        self.draw_rect(self.color, i, j)

class Floor(Tile):
    def __init__(self):
        super().__init__()
        self.floor_normal = pygame.image.load("./sprites/my_dungeon_tiles/floor.png")
        self.platform_floor = pygame.image.load("./sprites/my_dungeon_tiles/platform_floor.png")

        self.set_sprite(self.floor_normal)
        self.symbol = ' '

class Pit(Tile):
    def __init__(self):
        super().__init__()
        self.top = pygame.image.load("./sprites/my_dungeon_tiles/void_top.png")
        self.top_right = pygame.image.load("./sprites/my_dungeon_tiles/void_top_right.png")
        self.top_left = pygame.image.load("./sprites/my_dungeon_tiles/void_top_left.png")
        self.middle = pygame.image.load("./sprites/my_dungeon_tiles/void_middle.png")
        self.left = pygame.image.load("./sprites/my_dungeon_tiles/void_left.png")
        self.right = pygame.image.load("./sprites/my_dungeon_tiles/void_right.png")
        self.bottom_left = pygame.image.load("./sprites/my_dungeon_tiles/void_bottom_left.png")
        self.bottom_right = pygame.image.load("./sprites/my_dungeon_tiles/void_bottom_right.png")
        self.bottom = pygame.image.load("./sprites/my_dungeon_tiles/void_bottom.png")
        self.color = brown 
        self.symbol = 'p'

    def draw(self, i, j):
        self.draw_rect(self.color, i, j)

class Door(Tile):
    def __init__(self, direction):
        super().__init__()
        self.left = pygame.image.load("./sprites/my_dungeon_tiles/left_door.png")
        self.right = pygame.image.load("./sprites/my_dungeon_tiles/right_door.png")
        self.up = pygame.image.load("./sprites/my_dungeon_tiles/top_door.png")
        self.down = pygame.image.load("./sprites/my_dungeon_tiles/bottom_door.png")
        self.color = gray #(60,60,60) 
        self.direction = direction
        self.symbol = self.set_dir()
        self.set_sprite()
    
    def set_sprite(self):
        dir = None
        if self.direction == Direction.UP:
            dir = self.up
        elif self.direction == Direction.DOWN:
            dir = self.down
        elif self.direction == Direction.LEFT:
            dir = self.left
        elif self.direction == Direction.RIGHT:
            dir = self.right
        super().set_sprite(dir)
        
    def set_dir(self):
        if self.direction == Direction.UP:
            return 'U'
        elif self.direction == Direction.DOWN:
            return 'D'
        elif self.direction == Direction.LEFT:
            return 'L'
        elif self.direction == Direction.RIGHT:
            return 'R'
        return "Error in setting direction"
 
class LockedDoor(Door):
    def __init__(self, direction): # TO DO : Draw sprite!
        super().__init__(direction)
        self.color = gold
        self.locked = True
    
    def unlock(self):
        self.locked = False
        self.color = gray

    def draw(self, i, j):
        self.draw_rect(self.color, i, j)

class Block(Tile):
    def __init__(self):
        super().__init__()

class Pillar(Tile):
    def __init__(self):
        self.img = pygame.image.load("./sprites/my_dungeon_tiles/pillar.png")
        super().__init__()
        self.set_sprite(self.img)
        self.symbol = 'P'
