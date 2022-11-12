#!/bin/env python3

import pgzrun
import pygame
import math
from screeninfo import get_monitors

monitors = get_monitors()

# WIDTH = monitors[0].width
# HEIGHT = monitors[0].height

WIDTH = 800
HEIGHT = 800

CENTER = (WIDTH/2, HEIGHT/2)
RADIUS = min(WIDTH/2, HEIGHT/2)

D = RADIUS/5 # distance between 2 balls
A = D * math.sqrt(3)/2 # height between 2 lines

EMPTY = 0
BLACK = 1
WHITE = 2

class Space:
    state = EMPTY
    i = None
    j = None

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def pos(self):
        x = CENTER[0] + (self.j-4)*D + abs(self.i-4)*D/2
        y = CENTER[1] + (self.i-4)*A
        return (x,y)

    def draw(self):
        pos = self.pos()
        rad = RADIUS/12
        if self.state == BLACK:
            screen.draw.filled_circle(pos, rad, (0,0,0))
        elif self.state == WHITE:
            screen.draw.filled_circle(pos, rad, (255,255,255))
        else:
            screen.draw.circle(pos, rad, (200,200,200))



class Board:
    lines = []

    def __init__(self):
        # create empty spaces
        for n in [5,6,7,8,9,8,7,6,5]:
            line = []
            for j in range(n):
                line.append(Space(len(self.lines), j))
            self.lines.append(line)

        for space in self.lines[0] + self.lines[1] + self.lines[2][2:5]:
            space.state = BLACK
        for space in self.lines[8] + self.lines[7] + self.lines[6][2:5]:
            space.state = WHITE
    
    def draw(self):
        for line in self.lines:
            for space in line:
                space.draw()





board = Board()

def draw():
    # screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    screen.clear()
    screen.fill((0,128,200))
    # screen.draw.filled_rect(Rect((10,10),(60,10)), (128,128,128))
    board.draw()



pgzrun.go()