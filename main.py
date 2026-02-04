import pygame as g
import numpy as np
from scipy.signal import convolve2d

board_shape = (8, 8)
num_mines = 10
mine_board = np.zeros(shape=board_shape)

mine_positions = np.random.choice(mine_board.size, num_mines, replace=False)

mine_board.flat[mine_positions] = -1

mines_only = (mine_board == -1).astype(int)

kernel = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]])

neighbour_count = convolve2d(mines_only, kernel, mode='same', boundary='fill')
neighbour_count -= mines_only

board = np.where(mine_board == -1, -1, neighbour_count)

print(board)

# Pygame initialization as done in the documentation

g.init()
screen = g.display.set_mode((1200, 720))
clock = g.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in g.event.get():
        if event.type == g.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    g.display.flip()

    clock.tick(60)  # limits FPS to 60

g.quit()

