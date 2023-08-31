from fund_values import *
from Room import *

class Map:
    # holds the whole map of rooms
    def __init__(self, map_type="Level1"):
        if map_type == "Testing":
          self.rooms = self.get_testing_rooms()
        elif map_type == "Level1":
          self.rooms = self.get_rooms()
        self.cur_room = self.rooms[0]
        self.add_doors()

    def get_testing_rooms(self):
        b1 = BasicRoom()
        return [b1]
    
    def get_rooms(self):
        '''
          B
          |
        B-P-B 
          |
          B-P
        
        '''
        b1, b2, b3, b4 = BasicRoom(), BasicRoom(), PitRoom(), BasicRoom()
        #b1.add_item(Key(11,8))
        #b1.add_item(Heart(4,8, None, True))
        #b1.add_item(Chest(5,7,None,True))
        slime = Slime(8,8)
        slime.add_holding_item(Key)
        b1.add_item(Gold(5,5,None,True))
        b1.add_item(Chest(7,7,None,True, Key))
        b1.add_item(Chest(5,7, None, True, Gold))
        b1.add_item(Chest(9,7, None, True, Heart))
        b4.add_enemy(slime)

        p1 = PillarRoom()
        pp1 = PillarPitRoom()
        self.connect_east_west(pp1, b1, False)
        w1 = WallsRoom1()
        w2 = WallsRoom2()
        for i in range(0,10):
          w2.add_enemy(Slime(4,4))
          w2.add_enemy(Bat(6,6))
        self.connect_east_west(b1, w1, False)
        self.connect_north_south(w1, w2, False)

        self.connect_east_west(b4, p1, False) # east room then west room
        self.connect_east_west(p1, b2, False)
        self.connect_north_south(b3, p1, True) # north room then south room
        self.connect_north_south(p1, b1, False)
        
        return [b1, b2, b3, b4, p1, pp1, w1, w2]
    
    def connect_north_south(self, north_room, south_room, locked):
        # adds a door or locked door between 2 rooms, connecting the 2 rooms
        south_room.adj_rooms[0] = north_room
        north_room.adj_rooms[1] = south_room

        if locked:
            south_room.locked[0] = True
            north_room.locked[1] = True
      
    def connect_east_west(self, east_room, west_room, locked):
        # adds a door or locked door between 2 rooms, connecting the 2 rooms
        east_room.adj_rooms[2] = west_room
        west_room.adj_rooms[3] = east_room

        if locked:
            east_room.locked[2] = True
            west_room.locked[3] = True

    def add_doors(self):
        for room in self.rooms:
            room.add_doors()