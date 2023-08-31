from fund_values import *
#from Room import *

'''
Important screen info
WIDTH = 1020
HEIGHT = 780
NUM_TILES_WIDE = 17
NUM_TILES_TALL = 13
TILE_WIDTH = 60

So the grid is 17 by 13
'''
class Tilemap:
    def __init__(self, cur_room_tiles):
        #self.room_builder = RoomBuilder()
        self.cur_room_tiles = cur_room_tiles
        self.display_cur_room()
    
    def set_new_cur_room_tiles(self, new_cur_room_tiles):
        self.cur_room_tiles = new_cur_room_tiles
        self.display_cur_room()
                            

    def draw_tile(self, color, i, j): # i and j are the col and row respectively
        pygame.draw.rect(
                    screen,
                    color, 
                    pygame.Rect(i*TILE_WIDTH, j*TILE_WIDTH, TILE_WIDTH,TILE_WIDTH)
                )

    def display_cur_room(self):
        for i in range(0,NUM_TILES_TALL):
            for j in range(0,NUM_TILES_WIDE):
                tile = self.cur_room_tiles[i][j]
                print(tile.symbol, end = "")
            print()

    def draw(self):
        #print(f"Rows: {len(self.cur_map)} Cols: {len(self.cur_map[0])}")
        
        for i in range(0,NUM_TILES_TALL): # cols
            for j in range(0,NUM_TILES_WIDE): # rows
                #print(NUM_TILES_WIDE,i,j)
                tile = self.cur_room_tiles[i][j] # the first bracket is the row and second is col
                tile.draw(j,i)
                
                #self.draw_checkerboard(i,j)
                
    def draw_checkerboard(self, i, j):    
        if j%2==0:
            if i%2==0:
                self.draw_tile(blue, i, j)
            else:
                self.draw_tile(black, i, j)
        else:
            if i%2==0:
                self.draw_tile(black, i, j)
            else:
                self.draw_tile(blue, i, j)
