#!/bin/env python3

import pgzrun

WIDTH = 800
HEIGHT = 800

CENTER = (WIDTH/2, HEIGHT/2)
RADIUS = min(WIDTH/2, HEIGHT/2)


EMPTY = 0
BLACK = 1
WHITE = 2

class Space:
    state = EMPTY
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def neighbors(self):
        non_empty = []
        for case in [self.ul, self.ur, self.l, self.r, self.dl, self.dr]:
            if case:
                non_empty.append(case)
        return non_empty

    def nb_neighbors(self):
        return len(self.neighbors())

    def expand(cases):
        pass


class Board:
    lines = []

    def __init__(self):
        # create empty spaces
        for n in [5,6,7,8,9,8,7,6,5]:
            line = []
            for x in range(n):
                line.append(Space(x, len(self.lines)))
            self.lines.append(line)

        for space in self.lines[0] + self.lines[1] + self.lines[2][2:5]:
            space.state = BLACK
        for space in self.lines[8] + self.lines[7] + self.lines[6][2:5]:
            space.state = WHITE
    
    def draw(self):
        y = 20
        for line in self.lines:
            x = 20
            for space in line:
                x += RADIUS/5
                if space.state == BLACK:
                    screen.draw.filled_circle((x,y), RADIUS/12, (0,0,0))
                elif space.state == WHITE:
                    screen.draw.filled_circle((x,y), RADIUS/12, (255,255,255))
                else:
                    screen.draw.circle((x,y), RADIUS/12, (200,200,200))

            y += RADIUS/5




board = Board()

def draw():
    screen.clear()
    screen.fill((0,128,200))
    # screen.draw.filled_rect(Rect((10,10),(60,10)), (128,128,128))
    board.draw()



pgzrun.go()