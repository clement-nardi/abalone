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
BALL_RADIUS = RADIUS/12

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

    def x(self):
        return CENTER[0] + (self.j-4)*D + abs(self.i-4)*D/2

    def y(self):
        return CENTER[1] + (self.i-4)*A

    def pos(self):
        return (self.x(),self.y())

    def draw(self):
        pos = self.pos()
        if self.state == BLACK:
            screen.draw.filled_circle(pos, BALL_RADIUS, (0,0,0))
        elif self.state == WHITE:
            screen.draw.filled_circle(pos, BALL_RADIUS, (255,255,255))
        else:
            screen.draw.circle(pos, BALL_RADIUS, (200,200,200))

def distance(a, b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1]))


class Board:
    lines = []
    selected = None
    arrows = []
    hover_pos = None

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
        if self.selected:
            for dr in range(int(BALL_RADIUS/3)):
                screen.draw.circle(self.selected.pos(), BALL_RADIUS - dr/2, (0,200,100))
            for i, arrow in enumerate(self.arrows):
                arrow.draw()

    def get_space_at(self, pos):
        for line in self.lines:
            if abs(line[0].y()-pos[1]) < BALL_RADIUS:
                for space in line:
                    if distance(space.pos(),pos) < BALL_RADIUS:
                        return space
        return None

    def is_selectable(self, space):
        return space.state != EMPTY

    def arrow(self, angle, image):
        arrow = Actor(image, self.selected.pos(), anchor=('left', 'center'))
        arrow._orig_surf = pygame.transform.scale(arrow._orig_surf, (BALL_RADIUS*3/2, BALL_RADIUS*3/2))
        arrow._surf = arrow._orig_surf
        arrow._update_pos()

        x = math.cos(angle*math.pi/180)*BALL_RADIUS*3/4
        y = math.sin(angle*math.pi/180)*BALL_RADIUS*3/4
        arrow.angle = angle
        arrow.x += x
        arrow.y -= y
        return arrow


    def click_at(self, pos):
        clicked = self.get_space_at(pos)
        if clicked and not self.is_selectable(clicked):
            clicked = None
        self.selected = clicked
        self.set_arrows()
    
    def set_arrows(self):
        if self.selected:
            self.arrows = []
            count = 0
            hovered = None
            i = 0
            for n in range(6):
                arrow = self.arrow(n*60, 'arrow_right_green')
                if arrow.collidepoint(self.hover_pos):
                    count += 1
                    hovered = i
                
                self.arrows.append(arrow)
                i += 1
            if count == 1:
                self.arrows[hovered] = self.arrow(self.arrows[hovered].angle, 'arrow_right_red')

    def hover(self, pos):
        self.hover_pos = pos
        self.set_arrows()



board = Board()

def draw():
    # screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    screen.clear()
    screen.fill((0,50,200))
    # screen.draw.filled_rect(Rect((10,10),(60,10)), (128,128,128))
    board.draw()


def on_mouse_down(pos):
    board.click_at(pos)

def on_mouse_move(pos):
    board.hover(pos)


pgzrun.go()