from fund_values import *
from Tiles import * 

class RowBuilder:
    def __init__(self):
        self.background_row = [Background() for _ in range(NUM_TILES_WIDE)]
        self.wall_top_row = self.get_wall_top_row()
        
    def get_wall_top_row(self):
        wall_top_row = []
        wall_top_row.append(Background())
        for _ in range(1, NUM_TILES_WIDE-1):
            wall_top_row.append(Wall())
        wall_top_row.append(Background())
        return wall_top_row

    def get_floor_row(self, is_odd):
        floor_row = []
        floor_row.append(Background())
        floor_row.append(Wall())
        for i in range(2, NUM_TILES_WIDE-2):
            self.add_odd_floor_tile(floor_row, i, is_odd)
        floor_row.append(Wall())
        floor_row.append(Background())
        return floor_row

    def add_odd_floor_tile(self, floor_row, i, is_odd):
        if is_odd:
            if i%2 == 1:
                floor_row.append(Floor())
            else:
                floor_row.append(Floor())
        else:
            if i%2 == 0:
                floor_row.append(Floor())
            else:
                floor_row.append(Floor())

    def get_pillar_row(self, is_odd):
        # BWFFFWFFFFFWFFFWB
        # 0123456789

        pillar_row = []
        pillar_row.append(Background())
        pillar_row.append(Wall())
        for i in range(2, 5):
            self.add_odd_floor_tile(pillar_row, i, is_odd)
        pillar_row.append(Wall())
        for i in range(6, 11):
            self.add_odd_floor_tile(pillar_row, i, is_odd)
        pillar_row.append(Wall())
        for i in range(12, 15):
            self.add_odd_floor_tile(pillar_row, i, is_odd)
        pillar_row.append(Wall())
        pillar_row.append(Background())
        return pillar_row

   
    
    
        
    