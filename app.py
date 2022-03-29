import pygame
from pygame.locals import *
import random
import time

class Board:
    grid_colour = (0,0,0)
    background = (247, 217, 193)
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800

    # Change this to change the number of boxes/dimensino
    dim = 8

    blockSize = WINDOW_HEIGHT//dim
    MAX = 0
    

    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.grid = [[0 for i in range(self.dim)] for i in range(self.dim)]
        self.fill_grid()


    def make_grid(self, n):
        blockSize = self.blockSize
        for x in range(0, self.WINDOW_WIDTH, blockSize):
            for y in range(0, self.WINDOW_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.parent_window, self.grid_colour, rect, 1)
        pygame.display.flip()


    def get_row(self, x):
        return self.grid[x-1]


    def set_row(self, li, x):
        self.grid[x-1] = li


    def get_column(self, x):
        li = []
        for row in self.grid:
            li.append(row[x-1])
        return li
    

    def set_column(self, li, x):
        for row in range(self.dim):
            self.grid[row][x-1] = li[row]


    def no_zeros(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.grid[i][j] == 0:
                    return False
        return True


    def check_adjacent(self, li):
        for i in range(self.dim-1):
            if li[i] == li[i+1]:
                return True
        return False


    def is_full(self):
        for i in range(self.dim):
            if self.check_adjacent(self.get_row(i)):
                return False
            if self.check_adjacent(self.get_column(i)):
                return False
        return True


    def update_list(self, li, reverse=False):
        if reverse:
            li = li[::-1]
        ptr2 = self.dim - 1 
        ptr1 = self.dim - 2
        while ptr1 != -1:
            if li[ptr2] == 0 and li[ptr1] == 0:
                ptr1 -= 1
                continue
            if li[ptr2] == 0 and li[ptr1] != 0:
                li[ptr2] = li[ptr1]
                li[ptr1] = 0
                ptr1 -= 1
                continue
            if li[ptr1] == 0 and li[ptr2] != 0:
                ptr1 -= 1
                continue
                
            if li[ptr1] == li[ptr2]:
                li[ptr2] = 2 * li[ptr2]
                # Set Max value
                self.MAX = max(self.MAX, li[ptr2])
                li[ptr1] = 0
                ptr1-=1
                ptr2-=1
            else:
                ptr2-=1
                if ptr1 == ptr2:
                    ptr1-=1
        if reverse:
            return li[::-1]
        return li


    def write_text(self, text, location, color=(0,0,0), size=35):
        textFont = pygame.font.Font('freesansbold.ttf', size)
        textSurf = textFont.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = location
        self.parent_window.blit(textSurf, textRect)
        pygame.display.flip()


    def fill_grid(self):
        text_loc = self.blockSize
        loc_y = text_loc//2
        for x in range(self.dim):
            loc_x = text_loc//2
            for y in range(self.dim):
                temp_x, temp_y = loc_x - 45, loc_y - 45
                pygame.draw.rect(self.parent_window, self.background, pygame.Rect(temp_x, temp_y, 90, 90))
                if self.grid[x][y] != 0:
                    self.write_text(str(self.grid[x][y]), (loc_x, loc_y))
                loc_x += text_loc
            loc_y += text_loc
        pygame.display.flip()


    def get_random_index(self):
        n = random.randrange(0, self.dim * self.dim)
        return (n//self.dim, n%self.dim)


    def fill_random(self):
        i, j = self.get_random_index()
        while self.grid[i][j] != 0:
            i, j = self.get_random_index()
        self.grid[i][j] = random.choice([2, 4])
        self.fill_grid()


    def move_horizontal(self, reverse=False):
        flag = False
        for i in range(self.dim):
            previous = self.get_row(i)
            updated = self.update_list(previous, reverse)
            self.set_row(updated, i)
            if previous != updated:
                flag=True
        return flag


    def move_vertical(self, reverse=False):
        flag = False
        for i in range(self.dim):
            previous = self.get_column(i)
            updated = self.update_list(previous, reverse)
            self.set_column(updated, i)
            if previous != updated:
                flag=True
        return flag


class Game:
    # Change this to increase or decrease the Maximum value
    MAX = 2048

    width = 800
    height = 900
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        self.window.fill((247, 217, 193))
        self.board = Board(self.window)
        self.board.make_grid(self.board.dim)

    def run(self):
        running = True
        self.board.fill_random()
        self.board.fill_random()
        while running:
            for event in pygame.event.get():
                flag = False
                if event.type == KEYDOWN:
                    
                    if event.key == K_ESCAPE:
                        running = False
                        flag = True

                    if event.key == K_LEFT:
                        self.board.move_horizontal(True)
                        flag = True

                    if event.key == K_RIGHT:
                        self.board.move_horizontal()
                        flag = True

                    if event.key == K_UP:
                        self.board.move_vertical(True)
                        flag = True

                    if event.key == K_DOWN:
                        self.board.move_vertical()
                        flag = True

                    if flag:
                        self.board.fill_grid()
                        
                        # Maximum score achieved 
                        if self.MAX <= self.board.MAX:
                            running = False
                        has_no_zero = self.board.no_zeros()
                        if not has_no_zero:
                            self.board.fill_random()
                        if self.board.is_full() and has_no_zero:
                            running = False
                elif event.type == QUIT:
                    running = False
                if running == False:
                    self.board.write_text(f"GAME OVER.. Please wait", (self.width//2, self.width+50), (255, 0, 0), 20)
                    time.sleep(1)


if __name__ == "__main__":
    game = Game()
    game.run()

