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
flag_board = np.zeros(board_shape, dtype=bool)
game_over = False

print(board)

g.init()

CELL_SIZE = 80
GAP = 4
BORDER_RADIUS = max(3, min(10, int(CELL_SIZE * 0.12)))

GRID_WIDTH = board_shape[1] * CELL_SIZE
GRID_HEIGHT = board_shape[0] * CELL_SIZE

SIDEBAR_WIDTH = 250
PADDING = 40

SCREEN_WIDTH = GRID_WIDTH + SIDEBAR_WIDTH + PADDING * 2
SCREEN_HEIGHT = max(GRID_HEIGHT + PADDING * 2, 500)

OFFSET_X = PADDING
OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2

screen = g.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = g.time.Clock()
running = True

BACKGROUND_COLOR = (100, 100, 100)
CELL_COLOR = (200, 200, 200)
EMPTY_CELL_COLOR = (78, 91, 94)
UNREVEALED_CELL_COLOR = (180, 180, 180)
SHADOW_COLOR = (60, 60, 60)
MINE_COLOR = (220, 80, 80)
FLAG_COLOR = (255, 220, 80)
INCORRECT_FLAG_COLOR = (255, 100, 100)
BUTTON_COLOR = (150, 150, 150)
BUTTON_HOVER_COLOR = (170, 170, 170)
BUTTON_TEXT_COLOR = (255, 255, 255)

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
button_font = None

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
            
            if flag_board[row, col]:
                flag_radius = max(3, int(cell_width * 0.2))
                center_x = x + cell_width // 2
                center_y = y + cell_height // 2
                g.draw.circle(screen, FLAG_COLOR, (center_x, center_y), flag_radius)

def draw_game_over_grid():
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
            cell_value = board[row, col]
            
            if cell_value == 0:
                cell_color = EMPTY_CELL_COLOR
            else:
                cell_color = CELL_COLOR
            
            g.draw.rect(screen, SHADOW_COLOR, (x + 2, y + 2, cell_width, cell_height), border_radius=BORDER_RADIUS)
            g.draw.rect(screen, cell_color, (x, y, cell_width, cell_height), border_radius=BORDER_RADIUS)
            
            if cell_value == -1:
                mine_radius = max(3, int(cell_width * 0.25))
                center_x = x + cell_width // 2
                center_y = y + cell_height // 2
                g.draw.circle(screen, MINE_COLOR, (center_x, center_y), mine_radius)
            elif cell_value > 0:
                color = NUMBER_COLORS.get(int(cell_value), (0, 0, 0))
                text = font.render(str(int(cell_value)), True, color)
                text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                screen.blit(text, text_rect)
            
            if flag_board[row, col]:
                flag_radius = max(3, int(cell_width * 0.2))
                center_x = x + cell_width // 2
                center_y = y + cell_height // 2
                flag_color = INCORRECT_FLAG_COLOR if cell_value != -1 else FLAG_COLOR
                g.draw.circle(screen, flag_color, (center_x, center_y), flag_radius)

def draw_game_over_ui():
    global button_font
    if button_font is None:
        button_font = g.font.Font(None, 36)
    
    label_font = g.font.Font(None, 48)
    
    sidebar_x = OFFSET_X + GRID_WIDTH + 30
    
    game_over_text = label_font.render("GAME OVER", True, (255, 100, 100))
    game_over_rect = game_over_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH - 30) // 2, OFFSET_Y + 50))
    screen.blit(game_over_text, game_over_rect)
    
    timer_text = button_font.render("Timer: 00:00", True, (255, 255, 255))
    timer_rect = timer_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH - 30) // 2, OFFSET_Y + 120))
    screen.blit(timer_text, timer_rect)
    
    button_width = 180
    button_height = 50
    button_x = sidebar_x + (SIDEBAR_WIDTH - 30 - button_width) // 2
    
    restart_button_y = SCREEN_HEIGHT - 150
    exit_button_y = SCREEN_HEIGHT - 80
    
    mouse_pos = g.mouse.get_pos()
    
    restart_color = BUTTON_HOVER_COLOR if button_x <= mouse_pos[0] <= button_x + button_width and restart_button_y <= mouse_pos[1] <= restart_button_y + button_height else BUTTON_COLOR
    exit_color = BUTTON_HOVER_COLOR if button_x <= mouse_pos[0] <= button_x + button_width and exit_button_y <= mouse_pos[1] <= exit_button_y + button_height else BUTTON_COLOR
    
    g.draw.rect(screen, restart_color, (button_x, restart_button_y, button_width, button_height), border_radius=8)
    g.draw.rect(screen, exit_color, (button_x, exit_button_y, button_width, button_height), border_radius=8)
    
    restart_text = button_font.render("Restart", True, BUTTON_TEXT_COLOR)
    exit_text = button_font.render("Exit", True, BUTTON_TEXT_COLOR)
    
    restart_text_rect = restart_text.get_rect(center=(button_x + button_width // 2, restart_button_y + button_height // 2))
    exit_text_rect = exit_text.get_rect(center=(button_x + button_width // 2, exit_button_y + button_height // 2))
    
    screen.blit(restart_text, restart_text_rect)
    screen.blit(exit_text, exit_text_rect)
    
    return (button_x, restart_button_y, button_width, button_height), (button_x, exit_button_y, button_width, button_height)

def handle_click(mouse_x, mouse_y):
    global game_over
    col = (mouse_x - OFFSET_X) // CELL_SIZE
    row = (mouse_y - OFFSET_Y) // CELL_SIZE
    
    if 0 <= row < board_shape[0] and 0 <= col < board_shape[1]:
        if user_board[row, col] == -2 and not flag_board[row, col]:
            user_board[row, col] = board[row, col]
            if board[row, col] == -1:
                game_over = True

def handle_right_click(mouse_x, mouse_y):
    col = (mouse_x - OFFSET_X) // CELL_SIZE
    row = (mouse_y - OFFSET_Y) // CELL_SIZE
    
    if 0 <= row < board_shape[0] and 0 <= col < board_shape[1]:
        if user_board[row, col] == -2:
            flag_board[row, col] = not flag_board[row, col]

def restart_game():
    global board, user_board, flag_board, game_over, mine_board
    mine_board = np.zeros(shape=board_shape)
    mine_positions = np.random.choice(mine_board.size, num_mines, replace=False)
    mine_board.flat[mine_positions] = -1
    mines_only = (mine_board == -1).astype(int)
    neighbour_count = convolve2d(mines_only, kernel, mode='same', boundary='fill')
    neighbour_count -= mines_only
    board = np.where(mine_board == -1, -1, neighbour_count)
    user_board = np.full(board_shape, -2, dtype=int)
    flag_board = np.zeros(board_shape, dtype=bool)
    game_over = False

def handle_button_click(mouse_x, mouse_y, restart_rect, exit_rect):
    global running
    if restart_rect[0] <= mouse_x <= restart_rect[0] + restart_rect[2] and restart_rect[1] <= mouse_y <= restart_rect[1] + restart_rect[3]:
        restart_game()
    elif exit_rect[0] <= mouse_x <= exit_rect[0] + exit_rect[2] and exit_rect[1] <= mouse_y <= exit_rect[1] + exit_rect[3]:
        running = False

while running:
    for event in g.event.get():
        if event.type == g.QUIT:
            running = False
        elif event.type == g.MOUSEBUTTONDOWN:
            if game_over:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    sidebar_x = OFFSET_X + GRID_WIDTH + 30
                    button_width = 180
                    button_height = 50
                    button_x = sidebar_x + (SIDEBAR_WIDTH - 30 - button_width) // 2
                    restart_button_y = SCREEN_HEIGHT - 150
                    exit_button_y = SCREEN_HEIGHT - 80
                    restart_rect = (button_x, restart_button_y, button_width, button_height)
                    exit_rect = (button_x, exit_button_y, button_width, button_height)
                    handle_button_click(mouse_x, mouse_y, restart_rect, exit_rect)
            else:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    handle_click(mouse_x, mouse_y)
                elif event.button == 3:
                    mouse_x, mouse_y = event.pos
                    handle_right_click(mouse_x, mouse_y)

    screen.fill(BACKGROUND_COLOR)
    if game_over:
        draw_game_over_grid()
        draw_game_over_ui()
    else:
        draw_grid()
    g.display.flip()
    clock.tick(60)

g.quit()

