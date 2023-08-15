from fund_values import *
from Tiles import *
from RowBuilder import RowBuilder
from Skeleton import Skeleton

class Room:
    def __init__(self):
        self.adj_rooms = [None, None, None, None] # north, south, west, east
        self.tiles = []
        self.row_builder = RowBuilder()
        self.enemies = []
        self.set_start_enemies_list()

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def set_start_enemies_list(self):
        pass

    def enemy_alive_check(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                self.enemies.remove(enemy)

    def get_north_room(self):
        return self.adj_rooms[0]
    def get_south_room(self):
        return self.adj_rooms[1]
    def get_west_room(self):
        return self.adj_rooms[2]
    def get_east_room(self):
        return self.adj_rooms[3]

    def add_doors(self):
        north_door_x, north_door_y = 8,1
        south_door_x, south_door_y = 8,NUM_TILES_TALL-2
        west_door_x, west_door_y = 1,6
        east_door_x, east_door_y = NUM_TILES_WIDE-2,6

        if self.adj_rooms[0]: # add north door
            self.tiles[north_door_y][north_door_x] = UpDoor()
            print("Adding up door")
        if self.adj_rooms[1]: # add south door
            self.tiles[south_door_y][south_door_x] = DownDoor()
            print("Adding down door")
        if self.adj_rooms[2]: # add north door
            self.tiles[west_door_y][west_door_x] = LeftDoor()
        if self.adj_rooms[3]: # add south door
            self.tiles[east_door_y][east_door_x] = RightDoor()

class PillarRoom(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.pillar_room_tiles()

    def set_start_enemies_list(self):
        self.add_enemy(Skeleton(get_middle_coord(4,4), True))
        self.add_enemy(Skeleton(get_middle_coord(12,5), False))
    
    def pillar_room_tiles(self):
        # background
        # walls
        # floor x 2 0,1
        # pillar 2
        # floor x 3 3,4,5
        # pillar 6
        # floor x 2 7,8
        # walls
        # background
        
        cur_room = []
        cur_room.append(self.row_builder.background_row)
        cur_room.append(copy(self.row_builder.wall_top_row))
        #cur_room.append(self.row_builder.get_wall_with_door_row(True))
        for i in range(0,9):
            is_odd = (i%2 == 1)
            if i == 2 or i == 6:
                cur_room.append(self.row_builder.get_pillar_row(is_odd))
            else:
                cur_room.append(self.row_builder.get_floor_row(is_odd))

        #cur_room.append(self.row_builder.get_wall_with_door_row(False))
        cur_room.append(copy(self.row_builder.wall_top_row))
        cur_room.append(self.row_builder.background_row)
        return cur_room

class BasicRoom(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.basic_room_tiles()

    def set_start_enemies_list(self):
        self.add_enemy(Skeleton(get_middle_coord(8,4), True))
        
    def basic_room_tiles(self):
        cur_room = []
        cur_room.append(self.row_builder.background_row)
        cur_room.append(copy(self.row_builder.wall_top_row))
        #cur_room.append(self.row_builder.get_wall_with_door_row(True))
        for i in range(NUM_TILES_TALL-4):
            if i%2==0:
                cur_room.append(self.row_builder.get_floor_row(False))
            else:
                cur_room.append(self.row_builder.get_floor_row(True))
        cur_room.append(copy(self.row_builder.wall_top_row))
        #cur_room.append(self.row_builder.get_wall_with_door_row(False))
        cur_room.append(self.row_builder.background_row)
        return cur_room