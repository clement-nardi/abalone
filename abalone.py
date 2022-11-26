#!/bin/env python3

import pgzrun
import pygame
import math
from screeninfo import get_monitors

import pygame.math

monitors = get_monitors()

# WIDTH = monitors[0].width
# HEIGHT = monitors[0].height

WIDTH = 1280
HEIGHT = 720

CENTER = pygame.Vector2(WIDTH * 3 / 7, HEIGHT / 2)
RADIUS = min(CENTER[0], CENTER[1])

D = RADIUS / 5  # distance between 2 balls
A = D * math.sqrt(3) / 2  # height between 2 lines
BALL_RADIUS = RADIUS / 12

EMPTY = 0
BLACK = 1
WHITE = 2


def draw_ball(pos, state):
    if state == BLACK:
        screen.draw.filled_circle(pos, BALL_RADIUS, (0, 0, 0))
    elif state == WHITE:
        screen.draw.filled_circle(pos, BALL_RADIUS, (255, 255, 255))
    else:
        screen.draw.circle(pos, BALL_RADIUS, (200, 200, 200))


class Space:
    state = EMPTY
    i = None
    j = None

    def __init__(self, i, j):
        self.i = i
        self.j = j

    @property
    def line(self):
        return self.i

    @property
    def diag1(self):
        if self.i >= 4:
            return self.j
        return self.j + 4 - self.i

    @property
    def diag2(self):
        return 12 - self.line - self.diag1

    def x(self):
        return CENTER[0] + (self.j - 4) * D + abs(self.i - 4) * D / 2

    def y(self):
        return CENTER[1] + (self.i - 4) * A

    def pos(self):
        return pygame.Vector2(self.x(), self.y())

    def draw(self):
        draw_ball(self.pos(), self.state)


class Board:

    def __init__(self):
        self.lines = []
        self.selected = []
        self.arrows = []
        self.hover_pos = None
        self.hover_idx = None
        self.current_player = WHITE

        # create empty spaces
        for n in [5, 6, 7, 8, 9, 8, 7, 6, 5]:
            line = []
            for j in range(n):
                line.append(Space(len(self.lines), j))
            self.lines.append(line)

        for space in self.lines[0] + self.lines[1] + self.lines[2][2:5]:
            space.state = BLACK
        for space in self.lines[8] + self.lines[7] + self.lines[6][2:5]:
            space.state = WHITE

    def count_color(self, color):
        count = 0
        for line in self.lines:
            for space in line:
                if space.state == color:
                    count += 1
        return count

    def draw(self):
        pos = pygame.Vector2(WIDTH * 5 / 6, HEIGHT / 4)
        for color in [BLACK, WHITE]:
            missing = 14 - self.count_color(color)
            if missing >= 6:
                if color == WHITE:
                    winner = "Black"
                else:
                    winner = "White"
                screen.draw.text(winner + " wins!!", center=(WIDTH/2, HEIGHT/2), fontsize=RADIUS/2)
                self.current_player = None
                return
            rel_pos = pygame.Vector2(-D * 3 / 4, 0)
            for n in range(missing):
                draw_ball(pos + rel_pos, color)
                rel_pos = rel_pos.rotate(60)
            pos[1] += HEIGHT / 2
        for line in self.lines:
            for space in line:
                space.draw()
        for ball in self.selected:
            for dr in range(int(BALL_RADIUS / 3)):
                screen.draw.circle(ball.pos(), BALL_RADIUS - dr / 2, (0, 200, 100))
        for i, arrow in enumerate(self.arrows):
            arrow.draw()

    def get_space_at(self, pos):
        for line in self.lines:
            if abs(line[0].y() - pos[1]) < BALL_RADIUS:
                for space in line:
                    if space.pos().distance_to(pos) < BALL_RADIUS:
                        return space
        return None

    def is_selectable(self, space):
        return space.state == self.current_player

    def arrow(self, pos, angle, image):
        arrow = Actor(image, pos, anchor=("left", "center"))
        arrow._orig_surf = pygame.transform.scale(
            arrow._orig_surf, (BALL_RADIUS * 3 / 2, BALL_RADIUS * 3 / 2)
        )
        arrow._surf = arrow._orig_surf
        arrow._update_pos()

        x = math.cos(angle * math.pi / 180) * BALL_RADIUS * 3 / 4
        y = math.sin(angle * math.pi / 180) * BALL_RADIUS * 3 / 4
        arrow.angle = angle
        arrow.x += x
        arrow.y -= y
        return arrow

    def neighbor_coordinates(self, space, angle):
        line = space.i
        diagonal = space.j
        new_line = line
        new_diagonal = diagonal
        if angle in [60, 120]:
            new_line = line - 1
            if line <= 4:
                if angle == 60:
                    new_diagonal = diagonal
                else:
                    new_diagonal = diagonal - 1
            else:
                if angle == 60:
                    new_diagonal = diagonal + 1
                else:
                    new_diagonal = diagonal
        elif angle in [240, 300]:
            new_line = line + 1

            if line >= 4:
                if angle == 300:
                    new_diagonal = diagonal
                else:
                    new_diagonal = diagonal - 1
            else:
                if angle == 300:
                    new_diagonal = diagonal + 1
                else:
                    new_diagonal = diagonal
        else:
            new_line = line
            if angle == 0:
                new_diagonal += 1
            else:
                new_diagonal -= 1
        return (new_line, new_diagonal)

    def neighbor(self, space, angle):
        coords = self.sanitize(self.neighbor_coordinates(space, angle))
        if coords:
            return self.lines[coords[0]][coords[1]]
        return None

    def sanitize(self, coordinates):
        line = coordinates[0]
        diagonal = coordinates[1]
        if line >= 0 and line < len(self.lines):
            if diagonal >= 0 and diagonal < len(self.lines[line]):
                return coordinates
        return None

    def switch_player(self):
        if self.current_player == WHITE:
            self.current_player = BLACK
        else:
            self.current_player = WHITE

    def move(self, selection, angle):
        current_space = selection
        previous_state = EMPTY
        while True:
            temp = current_space.state
            current_space.state = previous_state
            previous_state = temp
            if previous_state == EMPTY:
                break
            destination_space = self.neighbor(current_space, angle)
            if not destination_space:
                break
            current_space = destination_space

    def can_move(self, angle):
        if not self.selected:
            return False
        if len(self.selected) == 1:
            current_space = self.selected[0]
            player_color = current_space.state
            count_self = 1
            while True:
                current_space = self.neighbor(current_space, angle)
                if not current_space:
                    return False  # cannot push one's balls out of the board
                if current_space.state != player_color:
                    break
                count_self += 1
            if count_self > 3:
                return False  # cannot push more than 3 of one's balls
            opponent_color = current_space.state
            if opponent_color == EMPTY:
                return True  # just move one's balls around
            count_opponent = 1
            while True:
                current_space = self.neighbor(current_space, angle)
                if not current_space or current_space.state != opponent_color:
                    break
                count_opponent += 1
            if not current_space or current_space.state == EMPTY:
                if count_opponent < count_self:
                    return True
            return False
        else:
            for space in self.selected:
                neighbor = self.neighbor(space, angle)
                if not neighbor or neighbor.state != EMPTY:
                    return False
            return True

    def can_be_selected_together(self, s1, s2):
        if s1.state != s2.state:
            return False
        if s1 == s2:
            return False
        if s1.line == s2.line and abs(s1.diag1 - s2.diag1) <= 2:
            return True
        if s1.diag1 == s2.diag1 and abs(s1.line - s2.line) <= 2:
            return True
        if s1.diag2 == s2.diag2 and abs(s1.line - s2.line) <= 2:
            return True
        return False

    def multi_select(self, s1, s2):
        for n in range(6):
            angle = n * 60
            neighbor = self.neighbor(s1, angle)
            if not neighbor:
                continue
            if neighbor.state != s1.state:
                continue
            if neighbor == s2:
                return [s1, s2]
            next_neighbor = self.neighbor(neighbor, angle)
            if not next_neighbor:
                continue
            if next_neighbor.state != s1.state:
                continue
            if next_neighbor == s2:
                return [s1, neighbor, s2]
        return None

    def set_not_selection(self):
        self.selected = []
        self.hover_idx = None
        self.arrows = []

    def click_at(self, pos):
        if self.current_player == None:
            self.__init__()
            return

        if self.hover_idx != None:
            for ball in self.selected:
                self.move(ball, self.arrows[self.hover_idx].angle)
            self.set_not_selection()
            self.switch_player()
            return

        clicked = self.get_space_at(pos)
        if not clicked:
            self.set_not_selection()
            return

        if len(self.selected) == 1:
            new_selection = self.multi_select(self.selected[0], clicked)
            if new_selection:
                self.selected = new_selection
                self.set_arrows()
                return

        if self.is_selectable(clicked):
            self.selected = [clicked]
            self.set_arrows()
        else:
            self.set_not_selection()

    def set_arrows(self):
        if not self.selected:
            return
        pos = (
            (self.selected[0].pos()[0] + self.selected[-1].pos()[0]) / 2,
            (self.selected[0].pos()[1] + self.selected[-1].pos()[1]) / 2,
        )
        self.arrows = []
        count = 0
        hovered = None
        i = 0
        for n in range(6):
            angle = n * 60
            if self.can_move(angle):
                arrow = self.arrow(pos, angle, "arrow_right_green")
                if arrow.collidepoint(self.hover_pos):
                    count += 1
                    hovered = i

                self.arrows.append(arrow)
                i += 1
        if count == 1:
            self.arrows[hovered] = self.arrow(
                pos, self.arrows[hovered].angle, "arrow_right_red"
            )
            self.hover_idx = hovered
        else:
            self.hover_idx = None

    def hover(self, pos):
        self.hover_pos = pos
        self.set_arrows()


board = Board()


def draw():
    # screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    screen.clear()
    screen.fill((0, 50, 200))
    # screen.draw.filled_rect(Rect((10,10),(60,10)), (128,128,128))
    board.draw()


def on_mouse_down(pos):
    board.click_at(pos)


def on_mouse_move(pos):
    board.hover(pos)


pgzrun.go()
