import pygame, sys
from enum import Enum
from pygame.locals import *
from copy import copy

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

FPS = 60
clock = pygame.time.Clock()

# colors 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
light_blue = (0, 0, 150)
green = (0, 255, 0)
gray = (178, 190, 181)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NOT_MOVING = 5

def get_top_left_coord(i, j): # 
    return [i*TILE_WIDTH, j*TILE_WIDTH]
def get_middle_coord(i, j):
    return [i*TILE_WIDTH + TILE_WIDTH/2, j*TILE_WIDTH + TILE_WIDTH/2]
def draw_point(i,j):
    pygame.draw.circle(screen, red, get_middle_coord(i,j), 5)