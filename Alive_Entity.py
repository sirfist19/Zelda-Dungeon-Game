# this is the base class for anything that is alive
from fund_values import *

class Alive_Entity:
    def __init__(self, name, health, attack, movement_speed, coord):
        self.name = name
        self.max_health = health
        self.health = self.max_health
        self.alive = True
        self.attack = attack
        self.moving_dir = Direction.NOT_MOVING
        self.prev_moving_dir = Direction.NOT_MOVING
        self.movement_speed = movement_speed
        self.coord = coord

    def is_alive(self):
        if self.health <= 0:
            return False
        return True
    
    def damage(self, amt):
        self.health -= amt
        if self.health <= 0:
            self.health = 0
            self.alive = False
    
    def heal(self, amt):
        self.health += amt
        if self.health > self.max_health:
            self.health = self.max_health

    def move(self):
        if self.moving_dir == Direction.UP:
            self.coord[1] -= self.movement_speed
        elif self.moving_dir == Direction.DOWN:
            self.coord[1] += self.movement_speed
        elif self.moving_dir == Direction.LEFT:
            self.coord[0] -= self.movement_speed
        elif self.moving_dir == Direction.RIGHT:
            self.coord[0] += self.movement_speed

    def move_opposite(self):
        if self.moving_dir == Direction.UP:
            self.coord[1] += self.movement_speed
        elif self.moving_dir == Direction.DOWN:
            self.coord[1] -= self.movement_speed
        elif self.moving_dir == Direction.LEFT:
            self.coord[0] += self.movement_speed
        elif self.moving_dir == Direction.RIGHT:
            self.coord[0] -= self.movement_speed

    def wall_bounce(self, thing_center, wall_center):
        if thing_center[0] > wall_center[0] + TILE_WIDTH/2: # move right
            #print("Hit wall from left, going right")
            self.coord[0] += self.movement_speed
        if thing_center[0] < wall_center[0] - TILE_WIDTH/2: # move left
            #print("Hit wall from right, going left")
            self.coord[0] -= self.movement_speed
        if thing_center[1] > wall_center[1] + TILE_WIDTH/2: # move down
            #print("Hit wall from up, going down")
            self.coord[1] += self.movement_speed
        if thing_center[1] < wall_center[1] - TILE_WIDTH/2: # move up
            #print("Hit wall from down, going up")
            self.coord[1] -= self.movement_speed
        #print("Hit wall")
        #self.move_opposite(3)

    def set_opposite_dir(self):
        if self.moving_dir == Direction.UP:
            self.set_moving_dir(Direction.DOWN)
        elif self.moving_dir == Direction.DOWN:
            self.set_moving_dir(Direction.UP)
        elif self.moving_dir == Direction.LEFT:
            self.set_moving_dir(Direction.RIGHT)
        elif self.moving_dir == Direction.RIGHT:
            self.set_moving_dir(Direction.LEFT)

    def draw(self):
        raise NotImplementedError("Subclasses must override the draw method.")
    
    def set_moving_dir(self, dir):
        if type(dir) == Direction:
            self.moving_dir = dir
        else:
            print("Type Error: Moving direction not of type Direction.")
