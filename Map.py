from fund_values import *
from Room import *

class Map:
    # holds the whole map of rooms
    def __init__(self):
        self.rooms = self.get_rooms()
        self.cur_room = self.rooms[0]
        self.add_doors()

    def get_rooms(self):
        '''
          B
          |
        B-P-B
          |
          B
        
        '''
        b1, b2, b3, b4 = BasicRoom(), BasicRoom(), BasicRoom(), BasicRoom()
        p1 = PillarRoom()
        p1.adj_rooms[0] = b3
        p1.adj_rooms[1] = b1
        p1.adj_rooms[2] = b2
        p1.adj_rooms[3] = b4

        b1.adj_rooms[0] = p1
        b2.adj_rooms[3] = p1
        b3.adj_rooms[1] = p1
        b4.adj_rooms[2] = p1
        
        return [b1, b2, b3, b4, p1]
    
    def add_doors(self):
        for room in self.rooms:
            room.add_doors()