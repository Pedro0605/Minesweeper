import pygame as g

CELL_SIZE = 80
GAP = 4
BORDER_RADIUS = max(3, min(10, int(CELL_SIZE * 0.12)))

SIDEBAR_WIDTH = 250
PADDING = 40

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

class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        
        self.grid_width = model.board_shape[1] * CELL_SIZE
        self.grid_height = model.board_shape[0] * CELL_SIZE
        
        self.screen_width = self.grid_width + SIDEBAR_WIDTH + PADDING * 2
        self.screen_height = max(self.grid_height + PADDING * 2, 500)
        
        self.offset_x = PADDING
        self.offset_y = (self.screen_height - self.grid_height) // 2
        
        self.font = None
        self.button_font = None
    
    def draw_grid(self):
        if self.font is None:
            font_size = max(24, int(CELL_SIZE * 0.6))
            self.font = g.font.Font(None, font_size)
        
        for row in range(self.model.board_shape[0]):
            for col in range(self.model.board_shape[1]):
                x = self.offset_x + col * CELL_SIZE + GAP
                y = self.offset_y + row * CELL_SIZE + GAP
                cell_width = CELL_SIZE - GAP * 2
                cell_height = CELL_SIZE - GAP * 2
                user_value = self.model.user_board[row, col]
                
                if user_value == -2:
                    cell_color = UNREVEALED_CELL_COLOR
                elif user_value == 0:
                    cell_color = EMPTY_CELL_COLOR
                else:
                    cell_color = CELL_COLOR
                
                g.draw.rect(self.screen, SHADOW_COLOR, (x + 2, y + 2, cell_width, cell_height), border_radius=BORDER_RADIUS)
                g.draw.rect(self.screen, cell_color, (x, y, cell_width, cell_height), border_radius=BORDER_RADIUS)
                
                if user_value == -1:
                    mine_radius = max(3, int(cell_width * 0.25))
                    center_x = x + cell_width // 2
                    center_y = y + cell_height // 2
                    g.draw.circle(self.screen, MINE_COLOR, (center_x, center_y), mine_radius)
                elif user_value > 0:
                    color = NUMBER_COLORS.get(int(user_value), (0, 0, 0))
                    text = self.font.render(str(int(user_value)), True, color)
                    text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                    self.screen.blit(text, text_rect)
                
                if self.model.flag_board[row, col]:
                    flag_radius = max(3, int(cell_width * 0.2))
                    center_x = x + cell_width // 2
                    center_y = y + cell_height // 2
                    g.draw.circle(self.screen, FLAG_COLOR, (center_x, center_y), flag_radius)
    
    def draw_game_over_grid(self):
        if self.font is None:
            font_size = max(24, int(CELL_SIZE * 0.6))
            self.font = g.font.Font(None, font_size)
        
        for row in range(self.model.board_shape[0]):
            for col in range(self.model.board_shape[1]):
                x = self.offset_x + col * CELL_SIZE + GAP
                y = self.offset_y + row * CELL_SIZE + GAP
                cell_width = CELL_SIZE - GAP * 2
                cell_height = CELL_SIZE - GAP * 2
                cell_value = self.model.board[row, col]
                
                if cell_value == 0:
                    cell_color = EMPTY_CELL_COLOR
                else:
                    cell_color = CELL_COLOR
                
                g.draw.rect(self.screen, SHADOW_COLOR, (x + 2, y + 2, cell_width, cell_height), border_radius=BORDER_RADIUS)
                g.draw.rect(self.screen, cell_color, (x, y, cell_width, cell_height), border_radius=BORDER_RADIUS)
                
                if cell_value == -1:
                    mine_radius = max(3, int(cell_width * 0.25))
                    center_x = x + cell_width // 2
                    center_y = y + cell_height // 2
                    g.draw.circle(self.screen, MINE_COLOR, (center_x, center_y), mine_radius)
                elif cell_value > 0:
                    color = NUMBER_COLORS.get(int(cell_value), (0, 0, 0))
                    text = self.font.render(str(int(cell_value)), True, color)
                    text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                    self.screen.blit(text, text_rect)
                
                if self.model.flag_board[row, col]:
                    flag_radius = max(3, int(cell_width * 0.2))
                    center_x = x + cell_width // 2
                    center_y = y + cell_height // 2
                    flag_color = INCORRECT_FLAG_COLOR if cell_value != -1 else FLAG_COLOR
                    g.draw.circle(self.screen, flag_color, (center_x, center_y), flag_radius)
    
    def draw_game_over_ui(self):
        if self.button_font is None:
            self.button_font = g.font.Font(None, 36)
        
        label_font = g.font.Font(None, 48)
        
        sidebar_x = self.offset_x + self.grid_width + 30
        
        game_over_text = label_font.render("GAME OVER", True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH - 30) // 2, self.offset_y + 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        timer_text = self.button_font.render("Timer: 00:00", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH - 30) // 2, self.offset_y + 120))
        self.screen.blit(timer_text, timer_rect)
        
        button_width = 180
        button_height = 50
        button_x = sidebar_x + (SIDEBAR_WIDTH - 30 - button_width) // 2
        
        restart_button_y = self.screen_height - 150
        exit_button_y = self.screen_height - 80
        
        mouse_pos = g.mouse.get_pos()
        
        restart_color = BUTTON_HOVER_COLOR if button_x <= mouse_pos[0] <= button_x + button_width and restart_button_y <= mouse_pos[1] <= restart_button_y + button_height else BUTTON_COLOR
        exit_color = BUTTON_HOVER_COLOR if button_x <= mouse_pos[0] <= button_x + button_width and exit_button_y <= mouse_pos[1] <= exit_button_y + button_height else BUTTON_COLOR
        
        g.draw.rect(self.screen, restart_color, (button_x, restart_button_y, button_width, button_height), border_radius=8)
        g.draw.rect(self.screen, exit_color, (button_x, exit_button_y, button_width, button_height), border_radius=8)
        
        restart_text = self.button_font.render("Restart", True, BUTTON_TEXT_COLOR)
        exit_text = self.button_font.render("Exit", True, BUTTON_TEXT_COLOR)
        
        restart_text_rect = restart_text.get_rect(center=(button_x + button_width // 2, restart_button_y + button_height // 2))
        exit_text_rect = exit_text.get_rect(center=(button_x + button_width // 2, exit_button_y + button_height // 2))
        
        self.screen.blit(restart_text, restart_text_rect)
        self.screen.blit(exit_text, exit_text_rect)
        
        return (button_x, restart_button_y, button_width, button_height), (button_x, exit_button_y, button_width, button_height)
    
    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        if self.model.game_over:
            self.draw_game_over_grid()
            self.draw_game_over_ui()
        else:
            self.draw_grid()
