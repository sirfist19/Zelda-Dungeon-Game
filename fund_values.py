import pygame, sys
from enum import Enum
from pygame.locals import *
from copy import copy
import random

pygame.init()

DRAW_HIT_BOXES = False
DRAW_WAYPOINTS = False

WIDTH = 1020
HEIGHT = 780
NUM_TILES_WIDE = 17
NUM_TILES_TALL = 13
TILE_WIDTH = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Zelda Dungeon')

MIDDLE_SCREEN_POS = (WIDTH/2, HEIGHT/2)
CURRENT_LEVEL = "Level1" # other options are "Testing"

FPS = 60
clock = pygame.time.Clock()

IFRAME_TIME = FPS*.2 # this is 12

# colors 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
light_blue = (0, 0, 150)
green = (0, 255, 0)
light_gray = (178, 190, 181)
gray = (60, 60, 60)
gold = (0xff, 0xd7, 0x00)
brown = (0x96, 0x4B, 0x00) #964B00

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NOT_MOVING = 5

class TileDirection(Enum):
    LEFT_TOP = 1
    TOP = 2
    RIGHT_TOP = 3
    LEFT = 4
    RIGHT = 5
    LEFT_BOTTOM = 6
    BOTTOM = 7
    RIGHT_BOTTOM = 8
    MIDDLE = 9

def get_opposite_dir(dir):
    if dir == Direction.UP:
        return Direction.DOWN
    elif dir == Direction.DOWN:
        return Direction.UP
    elif dir == Direction.LEFT:
        return Direction.RIGHT
    elif dir == Direction.RIGHT:
        return Direction.LEFT
    else:
        return Direction.NOT_MOVING

def get_top_left_coord(i, j): # 
    return [i*TILE_WIDTH, j*TILE_WIDTH]
def get_middle_coord(i, j):
    return [i*TILE_WIDTH + TILE_WIDTH/2, j*TILE_WIDTH + TILE_WIDTH/2]

def get_ij_from_coord(coord):
    x, y = coord
    return [x//TILE_WIDTH, y//TILE_WIDTH]

def draw_point(i,j):
    pygame.draw.circle(screen, green, get_middle_coord(i,j), 5)
                                         