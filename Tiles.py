from fund_values import *

class Tile:
    def __init__(self):
        pass

    def draw(self, color, i, j): # i and j are the col and row respectively
        # the tilemap calls this method on the derived tiles and the derived tiles draw this method to draw all the tiles
        pygame.draw.rect(
                    screen,
                    color, 
                    pygame.Rect(i*TILE_WIDTH, j*TILE_WIDTH, TILE_WIDTH,TILE_WIDTH)
    )
        
    def get_rect(self, i, j):
        return pygame.Rect(i*TILE_WIDTH, j*TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)

class Wall(Tile):
    def __init__(self):
        self.color = gray
        self.symbol = 'W'

    def draw(self, i, j):
        super().draw(self.color, i, j)

class Background(Tile):
    def __init__(self):
        self.color = black
        self.symbol = 'B'

    def draw(self, i, j):
        super().draw(self.color, i, j)

class Floor(Tile):
    def __init__(self, color):
        self.color = color #light_blue
        self.symbol = 'F'

    def draw(self, i, j):
        super().draw(self.color, i, j)

class UpDoor(Tile):
    def __init__(self):
        self.color = red #light_blue
        self.symbol = 'U'

    def draw(self, i, j):
        super().draw(self.color, i, j)
    
class DownDoor(Tile):
    def __init__(self):
        self.color = green #light_blue
        self.symbol = 'D'

    def draw(self, i, j):
        super().draw(self.color, i, j)

class LeftDoor(Tile):
    def __init__(self):
        self.color = (60,60,60) #light_blue
        self.symbol = 'L'

    def draw(self, i, j):
        super().draw(self.color, i, j)
    
class RightDoor(Tile):
    def __init__(self):
        self.color = (0, 13, 56) #light_blue
        self.symbol = 'R'

    def draw(self, i, j):
        super().draw(self.color, i, j)

