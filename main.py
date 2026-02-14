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
user_board = np.full(board_shape, -2, dtype=int)

print(board)

g.init()
screen = g.display.set_mode((1200, 720))
clock = g.time.Clock()
running = True

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
PADDING = 40
GAP = 4

max_cell_width = (SCREEN_WIDTH - 2 * PADDING) // board_shape[1]
max_cell_height = (SCREEN_HEIGHT - 2 * PADDING) // board_shape[0]
CELL_SIZE = min(max_cell_width, max_cell_height)
BORDER_RADIUS = max(3, min(10, int(CELL_SIZE * 0.12)))

GRID_WIDTH = board_shape[1] * CELL_SIZE
GRID_HEIGHT = board_shape[0] * CELL_SIZE
OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2

BACKGROUND_COLOR = (100, 100, 100)
CELL_COLOR = (200, 200, 200)
EMPTY_CELL_COLOR = (78, 91, 94)
UNREVEALED_CELL_COLOR = (180, 180, 180)
SHADOW_COLOR = (60, 60, 60)
MINE_COLOR = (220, 80, 80)

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
        font_size = max(24, int(CELL_SIZE * 0.6))
        font = g.font.Font(None, font_size)
    
    for row in range(board_shape[0]):
        for col in range(board_shape[1]):
            x = OFFSET_X + col * CELL_SIZE + GAP
            y = OFFSET_Y + row * CELL_SIZE + GAP
            cell_width = CELL_SIZE - GAP * 2
            cell_height = CELL_SIZE - GAP * 2
            user_value = user_board[row, col]
            
            if user_value == -2:
                cell_color = UNREVEALED_CELL_COLOR
            elif user_value == 0:
                cell_color = EMPTY_CELL_COLOR
            else:
                cell_color = CELL_COLOR
            
            g.draw.rect(screen, SHADOW_COLOR, (x + 2, y + 2, cell_width, cell_height), border_radius=BORDER_RADIUS)
            g.draw.rect(screen, cell_color, (x, y, cell_width, cell_height), border_radius=BORDER_RADIUS)
            
            if user_value == -1:
                mine_radius = max(3, int(cell_width * 0.25))
                center_x = x + cell_width // 2
                center_y = y + cell_height // 2
                g.draw.circle(screen, MINE_COLOR, (center_x, center_y), mine_radius)
            elif user_value > 0:
                color = NUMBER_COLORS.get(int(user_value), (0, 0, 0))
                text = font.render(str(int(user_value)), True, color)
                text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                screen.blit(text, text_rect)

def handle_click(mouse_x, mouse_y):
    col = (mouse_x - OFFSET_X) // CELL_SIZE
    row = (mouse_y - OFFSET_Y) // CELL_SIZE
    
    if 0 <= row < board_shape[0] and 0 <= col < board_shape[1]:
        if user_board[row, col] == -2:
            user_board[row, col] = board[row, col]

while running:
    for event in g.event.get():
        if event.type == g.QUIT:
            running = False
        elif event.type == g.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                handle_click(mouse_x, mouse_y)

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    g.display.flip()
    clock.tick(60)

g.quit()

