# this is the base class for anything that is alive
from fund_values import *
from Sprite import Sprite

class Alive_Entity:
    def __init__(self, name, health, attack, movement_speed, knockback_const, sprite):
        self.name = name
        self.max_health = health
        self.health = self.max_health
        self.alive = True
        self.attack = attack
        self.moving_dir = Direction.NOT_MOVING
        self.prev_moving_dir = Direction.NOT_MOVING
        self.movement_speed = movement_speed
        self.max_iFrame = IFRAME_TIME 
        self.iFrame_timer = 0
        self.knockback_const = knockback_const

        self.sprite = sprite

    def is_alive(self):
        if self.health <= 0:
            return False
        return True
    
    def damage(self, amt):
        if self.iFrame_timer == 0:
            self.health -= amt
            if self.health <= 0:
                self.health = 0
                self.alive = False
            self.iFrame_timer = self.max_iFrame
        #print(self.health, self.max_health)
    
    def decrease_iFrames(self):
        if self.iFrame_timer > 0:
            self.iFrame_timer -= 1

    def heal(self, amt):
        # if won't heal return false
        # if healing is successful return true
        if self.health >= self.max_health:
            return False
        
        self.health += amt
        if self.health > self.max_health:
            self.health = self.max_health
        return True

    def apply_knockback(self): # apply knockback to this entity
        opp_dir = get_opposite_dir(self.prev_moving_dir)
        self.sprite.move(opp_dir, self.knockback_const)

    def move(self):
        self.sprite.move(self.moving_dir, self.movement_speed)
        #print(self.name, self.moving_dir)

    def wall_bounce(self, thing_center, wall_center):
        if thing_center[0] > wall_center[0] + TILE_WIDTH/2: # move right
            #print("Hit wall from left, going right")
            self.sprite.move(Direction.RIGHT, self.movement_speed)
        if thing_center[0] < wall_center[0] - TILE_WIDTH/2: # move left
            #print("Hit wall from right, going left")
            self.sprite.move(Direction.LEFT, self.movement_speed)
        if thing_center[1] > wall_center[1] + TILE_WIDTH/2: # move down
            #print("Hit wall from up, going down")
            self.sprite.move(Direction.DOWN, self.movement_speed)
        if thing_center[1] < wall_center[1] - TILE_WIDTH/2: # move up
            #print("Hit wall from down, going up")
            self.sprite.move(Direction.UP, self.movement_speed)
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
