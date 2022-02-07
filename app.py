import pygame
from pygame.locals import *

class Board:
    grid_colour = (0,0,0)
    background = (247, 217, 193)
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 600
    dim = 4
    blockSize = WINDOW_HEIGHT//dim
    
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
        for row in range(self.dim):
            li.append(row[x-1])
        return li
    
    def set_column(self, li, x):
        for row in range(self.dim):
            self.grid[row][x-1] = li[row]

    def is_full(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.grid[i][j] == 0:
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
        
    def write_text(self, text, location, reset=False):
        textFont = pygame.font.Font('freesansbold.ttf', 60)
        textSurf = textFont.render(str(text), True, (0,0,0))
        if reset:
            textSurf = textFont.render(str(text), True, self.background)
        textRect = textSurf.get_rect()
        textRect.center = location
        self.parent_window.blit(textSurf, textRect)

    def fill_grid(self):
        text_loc = self.blockSize
        loc_y = text_loc//2
        for x in range(self.dim):
            loc_x = text_loc//2
            for y in range(self.dim):
                self.write_text(self.grid[x][y], (loc_x, loc_y))
                loc_x += text_loc
            loc_y += text_loc
        pygame.display.flip()

class Game:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((600, 700))
        self.window.fill((247, 217, 193))
        self.board = Board(self.window)
        self.board.make_grid(self.board.dim)
        

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        
                    if event.key == K_LEFT:
                        self.board.move_left()

                    if event.key == K_RIGHT:
                        self.board.move_right()

                    if event.key == K_UP:
                        self.board.move_up()

                    if event.key == K_DOWN:
                        self.board.move_down()

                elif event.type == QUIT:
                    running = False
                
                if self.board.is_full():
                    running = False


if __name__ == "__main__":
    game = Game()
    game.run()

