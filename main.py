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

g.init()
screen = g.display.set_mode((1200, 720))
clock = g.time.Clock()
running = True

CELL_SIZE = 80
GAP = 4
GRID_WIDTH = board_shape[1] * CELL_SIZE
GRID_HEIGHT = board_shape[0] * CELL_SIZE
OFFSET_X = (1200 - GRID_WIDTH) // 2
OFFSET_Y = (720 - GRID_HEIGHT) // 2

BACKGROUND_COLOR = (100, 100, 100)
CELL_COLOR = (200, 200, 200)
EMPTY_CELL_COLOR = (170, 190, 170)
SHADOW_COLOR = (60, 60, 60)

NUMBER_COLORS = {
    1: (100, 180, 120),
    2: (173, 129, 5),
    3: (220, 120, 120),
    4: (180, 120, 180),
    5: (160, 100, 160),
    6: (140, 80, 140),
    7: (120, 60, 120),
    8: (100, 40, 100)
}

font = None

def draw_grid():
    global font
    if font is None:
        font = g.font.Font(None, 48)
    
    for row in range(board_shape[0]):
        for col in range(board_shape[1]):
            x = OFFSET_X + col * CELL_SIZE + GAP
            y = OFFSET_Y + row * CELL_SIZE + GAP
            cell_width = CELL_SIZE - GAP * 2
            cell_height = CELL_SIZE - GAP * 2
            
            cell_value = board[row, col]
            cell_color = EMPTY_CELL_COLOR if cell_value == 0 else CELL_COLOR
            
            g.draw.rect(screen, SHADOW_COLOR, (x + 2, y + 2, cell_width, cell_height), border_radius=10)
            g.draw.rect(screen, cell_color, (x, y, cell_width, cell_height), border_radius=10)
            
            if cell_value > 0:
                color = NUMBER_COLORS.get(int(cell_value), (0, 0, 0))
                text = font.render(str(int(cell_value)), True, color)
                text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                screen.blit(text, text_rect)

while running:
    for event in g.event.get():
        if event.type == g.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    g.display.flip()
    clock.tick(60)

g.quit()

