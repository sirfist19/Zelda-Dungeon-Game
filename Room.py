from fund_values import *
from Tiles import *
from RowBuilder import RowBuilder
from Enemy import *
from Items import *

class Room:
    def __init__(self):
        self.adj_rooms = [None, None, None, None] # north, south, west, east
        self.locked = [False, False, False, False] # north, south, west, east
        self.tiles = []
        self.row_builder = RowBuilder()
        self.enemies = []
        self.set_start_enemies_list()
        self.items = []
        self.north_door_x, self.north_door_y = 8,1
        self.south_door_x, self.south_door_y = 8,NUM_TILES_TALL-2
        self.west_door_x, self.west_door_y = 1,6
        self.east_door_x, self.east_door_y = NUM_TILES_WIDE-2,6
        self.doors = [None, None, None, None]

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def convert_file_to_tiles(self, path):
        map = []
        tile_mapping = {
                'w': Wall(TileDirection.TOP),
                'W': Wall(TileDirection.BOTTOM),
                'p': Pit(), 
                ' ': Floor(),
                'B': Background(),
                'U': Door(Direction.UP), 
                'D': Door(Direction.DOWN),
                'L': Door(Direction.LEFT),
                'R': Door(Direction.RIGHT),
                'b': Block(), 
                'P': Pillar()} 
        start_path = "./rooms/"
        with open(start_path + path, "r") as file:
            #print("[")
            for row in file:
                cur_row = []
                for char in row:
                    if char == "\n":
                        break
                    mapped = tile_mapping[char]
                    cur_row.append(mapped)
                map.append(cur_row)
        return map

    def add_item(self, item):
        if isinstance(item, Item):
            print("Adding an item")
            self.items.append(item)

    def set_start_enemies_list(self):
        pass

    def enemy_alive_check(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                for item in enemy.drop_items():
                    self.items.append(item)
                self.enemies.remove(enemy)

    def get_adj_room(self, dir):
        if dir == Direction.UP:
            return self.get_north_room()
        if dir == Direction.DOWN:
            return self.get_south_room()
        if dir == Direction.LEFT:
            return self.get_west_room()
        if dir == Direction.RIGHT:
            return self.get_east_room()
        
    def get_north_room(self):
        return self.adj_rooms[0]
    def get_south_room(self):
        return self.adj_rooms[1]
    def get_west_room(self):
        return self.adj_rooms[2]
    def get_east_room(self):
        return self.adj_rooms[3]

    def add_doors(self):
        if self.adj_rooms[0]: # add north door
            if self.locked[0]:
                self.doors[0] = self.tiles[self.north_door_y][self.north_door_x] = LockedDoor(Direction.UP)
            else:
                self.doors[0] = self.tiles[self.north_door_y][self.north_door_x] = Door(Direction.UP)
            
        if self.adj_rooms[1]: # add south door
            if self.locked[1]:
                self.doors[1] = self.tiles[self.south_door_y][self.south_door_x] = LockedDoor(Direction.DOWN)
            else:  
                self.doors[1] = self.tiles[self.south_door_y][self.south_door_x] = Door(Direction.DOWN)

        if self.adj_rooms[2]: # add north door
            if self.locked[2]:
                self.doors[2] = self.tiles[self.west_door_y][self.west_door_x] = LockedDoor(Direction.LEFT)
            else:  
                self.doors[2] = self.tiles[self.west_door_y][self.west_door_x] = Door(Direction.LEFT)
        if self.adj_rooms[3]: # add south door
            if self.locked[3]:
                self.doors[3] = self.tiles[self.east_door_y][self.east_door_x] = LockedDoor(Direction.RIGHT)
            else:  
                self.doors[3] = self.tiles[self.east_door_y][self.east_door_x] = Door(Direction.RIGHT)

    def get_door(self, dir):
        if dir == Direction.UP:
            return self.doors[0]
        if dir == Direction.DOWN:
            return self.doors[1]
        if dir == Direction.LEFT:
            return self.doors[2]
        if dir == Direction.RIGHT:
            return self.doors[3]
    
    def unlock_door(self, door):
        door.unlock()
        #door.locked = False
        cur_door_dir = door.direction
        adj_room = self.get_adj_room(cur_door_dir)
        connected_door = adj_room.get_door(get_opposite_dir(cur_door_dir))
        #connected_door.locked = False
        connected_door.unlock()

class BasicRoom(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.convert_file_to_tiles("basic_room.txt") #self.basic_room_tiles()

    def set_start_enemies_list(self):
        #self.add_enemy(Skeleton(8,4, True))
        #self.add_enemy(Slime(8,4))
        pass

    def basic_room_tiles(self):
        #tiles = self.convert_file_to_tiles("basic_room.txt")
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

class PillarPitRoom(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.convert_file_to_tiles("pit_room1.txt")

class WallsRoom1(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.convert_file_to_tiles("walls1.txt")

class WallsRoom2(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.convert_file_to_tiles("walls2.txt")
       
class PillarRoom(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.convert_file_to_tiles("pillar_room.txt") #self.pillar_room_tiles()

    def set_start_enemies_list(self):
        heart_skele = Skeleton(4,6, True)
        heart_skele.add_holding_item(Heart)
        self.add_enemy(heart_skele)
        self.add_enemy(Skeleton(12,5, False))
    
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
        left_pillar_x = 5
        top_pillar_y = 4
        bottom_pillar_y = 8
        right_pillar_x = 11
        tiles = BasicRoom().basic_room_tiles()
        tiles[top_pillar_y][left_pillar_x] = Wall()
        tiles[top_pillar_y][right_pillar_x] = Wall()
        tiles[bottom_pillar_y][left_pillar_x] = Wall()
        tiles[bottom_pillar_y][right_pillar_x] = Wall()
        return tiles

class PitRoom(Room):
    def __init__(self):
        super().__init__()
        self.tiles = self.pit_room_tiles()
    
    def set_start_enemies_list(self):
        self.add_enemy(Bat(4, 4))
        self.add_enemy(Bat(8, 4))
        #self.add_enemy(Skeleton(get_middle_coord(12,5), False))
    
    def pit_room_tiles(self):
        # background
        # walls
        # floor x 2 0,1
        # pillar 2
        # floor x 3 3,4,5
        # pillar 6
        # floor x 2 7,8
        # walls
        # background
        left_pillar_x = 5
        top_pillar_y = 4
        bottom_pillar_y = 8
        right_pillar_x = 11
        tiles = BasicRoom().basic_room_tiles()
        tiles[top_pillar_y][left_pillar_x] = Pit()
        tiles[top_pillar_y][right_pillar_x] = Pit()
        tiles[bottom_pillar_y][left_pillar_x] = Pit()
        tiles[bottom_pillar_y][right_pillar_x] = Pit()
        return tiles
