from stat import FILE_ATTRIBUTE_SPARSE_FILE
import pygame
from pygame.locals import *
import time

class Board:
    grid_colour = (0,0,0)
    background = (247, 217, 193)
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 600
    dim = 4

    def __init__(self, parent_window):
        self.parent_window = parent_window


    def make_grid(self, n):
        blockSize = int((self.WINDOW_HEIGHT)/n)
        for x in range(0, self.WINDOW_WIDTH, blockSize):
            for y in range(0, self.WINDOW_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.parent_window, self.grid_colour, rect, 1)
        pygame.display.flip()

class Game:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((600, 700))
        self.window.fill((247, 217, 193))
        self.board = Board(self.window)
        self.board.make_grid(self.board.dim)
        
        time.sleep(2)

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

if __name__ == "__main__":
    game = Game()
    game.run()

    

    # running = True

    # while running:
    #     for event in pygame.event.get():
    #         if event.type == KEYDOWN:
    #             if event.key == K_ESCAPE:
    #                 running = False
    #         elif event.type == QUIT:
    #             running = False