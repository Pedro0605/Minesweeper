import pygame as g
import math

CELL_SIZE = 60
GAP = 3
BORDER_RADIUS = 5

SIDEBAR_WIDTH = 250
PADDING = 30

BACKGROUND_COLOR = (240, 240, 245)
CELL_COLOR = (255, 255, 255)
EMPTY_CELL_COLOR = (250, 250, 255)
UNREVEALED_CELL_COLOR = (220, 225, 235)
SHADOW_COLOR = (200, 205, 215)
MINE_COLOR = (220, 50, 50)
FLAG_COLOR = (255, 80, 80)
FLAG_POLE_COLOR = (100, 100, 100)
INCORRECT_FLAG_COLOR = (255, 150, 150)
PEEK_HIGHLIGHT_COLOR = (255, 240, 150)
BUTTON_COLOR = (100, 150, 255)
BUTTON_HOVER_COLOR = (120, 170, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
TEXT_COLOR = (50, 50, 60)
SUBTEXT_COLOR = (100, 100, 120)

NUMBER_COLORS = {
    1: (50, 120, 220),
    2: (50, 180, 80),
    3: (220, 50, 50),
    4: (120, 50, 180),
    5: (200, 100, 50),
    6: (50, 150, 180),
    7: (100, 100, 100),
    8: (150, 150, 150)
}

class GameView:
    def __init__(self, screen, model):
        """Initialize the game view with screen and model references."""
        self.screen = screen
        self.model = model
        self.cell_size = CELL_SIZE
        
        rows, cols = model.board_shape
        self.grid_width = cols * self.cell_size
        self.grid_height = rows * self.cell_size
        
        self.screen_width = self.grid_width + SIDEBAR_WIDTH + PADDING * 2
        self.screen_height = max(self.grid_height + PADDING * 2, 500)
        
        self.offset_x = PADDING
        self.offset_y = (self.screen_height - self.grid_height) // 2
        
        self.font = None
        self.title_font = None
        self.button_font = None
        self.peek_neighbors = None
        self.restart_rect = None
        self.exit_rect = None
    
    def update_dimensions(self, new_width, new_height):
        """Update view dimensions and scale cell size when window is resized."""
        self.screen_width = new_width
        self.screen_height = new_height
        
        rows, cols = self.model.board_shape
        available_w = max(1, new_width - SIDEBAR_WIDTH - PADDING * 2)
        available_h = max(1, new_height - PADDING * 2)
        new_cell_size = max(10, min(available_w // cols, available_h // rows))
        
        if new_cell_size != self.cell_size:
            self.cell_size = new_cell_size
            self.font = None
            self.title_font = None
            self.button_font = None
        
        self.grid_width = cols * self.cell_size
        self.grid_height = rows * self.cell_size
        self.offset_x = PADDING + max(0, (available_w - self.grid_width) // 2)
        self.offset_y = PADDING + max(0, (available_h - self.grid_height) // 2)
    
    def draw_flag(self, x, y, width, height):
        """Draw a flag icon."""
        center_x = x + width // 2
        center_y = y + height // 2
        flag_height = int(height * 0.5)
        flag_width = int(width * 0.4)
        
        pole_x = center_x - flag_width // 3
        pole_top = center_y - flag_height // 2
        pole_bottom = center_y + flag_height // 2 + 3
        
        g.draw.line(self.screen, FLAG_POLE_COLOR, (pole_x, pole_top), (pole_x, pole_bottom), 2)
        
        flag_points = [
            (pole_x, pole_top),
            (pole_x + flag_width, pole_top + flag_height // 3),
            (pole_x, pole_top + flag_height * 2 // 3)
        ]
        g.draw.polygon(self.screen, FLAG_COLOR, flag_points)
    
    def draw_mine(self, x, y, width, height):
        """Draw a mine icon."""
        center_x = x + width // 2
        center_y = y + height // 2
        mine_radius = max(8, int(width * 0.3))
        
        g.draw.circle(self.screen, MINE_COLOR, (center_x, center_y), mine_radius)
        
        for angle in [0, 45, 90, 135]:
            rad = math.radians(angle)
            x1 = center_x + int(math.cos(rad) * mine_radius * 1.4)
            y1 = center_y + int(math.sin(rad) * mine_radius * 1.4)
            x2 = center_x - int(math.cos(rad) * mine_radius * 1.4)
            y2 = center_y - int(math.sin(rad) * mine_radius * 1.4)
            g.draw.line(self.screen, MINE_COLOR, (x1, y1), (x2, y2), 2)
    
    def draw_grid(self):
        """Draw the game grid with cells, numbers, and flags."""
        cs = self.cell_size
        if self.font is None:
            font_size = max(10, int(cs * 0.55))
            self.font = g.font.Font(None, font_size)
            self.font.set_bold(True)
        
        for row in range(self.model.board_shape[0]):
            for col in range(self.model.board_shape[1]):
                x = self.offset_x + col * cs + GAP
                y = self.offset_y + row * cs + GAP
                cell_width = cs - GAP * 2
                cell_height = cs - GAP * 2
                user_value = self.model.user_board[row, col]
                
                is_highlighted = self.peek_neighbors and (row, col) in self.peek_neighbors
                
                if user_value == -2:
                    cell_color = UNREVEALED_CELL_COLOR
                elif user_value == 0:
                    cell_color = EMPTY_CELL_COLOR
                else:
                    cell_color = CELL_COLOR
                
                g.draw.rect(self.screen, SHADOW_COLOR, (x + 2, y + 2, cell_width, cell_height), border_radius=BORDER_RADIUS)
                g.draw.rect(self.screen, cell_color, (x, y, cell_width, cell_height), border_radius=BORDER_RADIUS)
                
                if user_value == -1:
                    self.draw_mine(x, y, cell_width, cell_height)
                elif user_value > 0:
                    color = NUMBER_COLORS.get(int(user_value), TEXT_COLOR)
                    text = self.font.render(str(int(user_value)), True, color)
                    text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                    self.screen.blit(text, text_rect)
                
                if self.model.flag_board[row, col]:
                    self.draw_flag(x, y, cell_width, cell_height)
                
                if is_highlighted:
                    overlay = g.Surface((cell_width, cell_height), g.SRCALPHA)
                    overlay.fill((*PEEK_HIGHLIGHT_COLOR, 100))
                    self.screen.blit(overlay, (x, y))
                    g.draw.rect(self.screen, PEEK_HIGHLIGHT_COLOR, (x, y, cell_width, cell_height), width=2, border_radius=BORDER_RADIUS)
        
        self.draw_sidebar()
    
    def draw_game_over_grid(self):
        """Draw the game grid when game is over, revealing all cells."""
        cs = self.cell_size
        if self.font is None:
            font_size = max(10, int(cs * 0.55))
            self.font = g.font.Font(None, font_size)
            self.font.set_bold(True)
        
        for row in range(self.model.board_shape[0]):
            for col in range(self.model.board_shape[1]):
                x = self.offset_x + col * cs + GAP
                y = self.offset_y + row * cs + GAP
                cell_width = cs - GAP * 2
                cell_height = cs - GAP * 2
                cell_value = self.model.board[row, col]
                
                if cell_value == 0:
                    cell_color = EMPTY_CELL_COLOR
                else:
                    cell_color = CELL_COLOR
                
                g.draw.rect(self.screen, SHADOW_COLOR, (x + 2, y + 2, cell_width, cell_height), border_radius=BORDER_RADIUS)
                g.draw.rect(self.screen, cell_color, (x, y, cell_width, cell_height), border_radius=BORDER_RADIUS)
                
                if cell_value == -1:
                    self.draw_mine(x, y, cell_width, cell_height)
                elif cell_value > 0:
                    color = NUMBER_COLORS.get(int(cell_value), TEXT_COLOR)
                    text = self.font.render(str(int(cell_value)), True, color)
                    text_rect = text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                    self.screen.blit(text, text_rect)
                
                if self.model.flag_board[row, col]:
                    if cell_value == -1:
                        self.draw_flag(x, y, cell_width, cell_height)
                    else:
                        g.draw.line(self.screen, INCORRECT_FLAG_COLOR, (x + 5, y + 5), 
                                   (x + cell_width - 5, y + cell_height - 5), 3)
                        g.draw.line(self.screen, INCORRECT_FLAG_COLOR, (x + cell_width - 5, y + 5), 
                                   (x + 5, y + cell_height - 5), 3)
    
    def _sidebar_center_x(self):
        """Return the horizontal center of the sidebar area."""
        sidebar_start = self.offset_x + self.grid_width + PADDING
        return sidebar_start + max(0, self.screen_width - sidebar_start - PADDING) // 2
    
    def draw_sidebar(self):
        """Draw the sidebar with stats and info."""
        sidebar_start = self.offset_x + self.grid_width + PADDING
        sidebar_w = max(1, self.screen_width - sidebar_start - PADDING)
        cx = sidebar_start + sidebar_w // 2
        
        if self.title_font is None:
            self.title_font = g.font.Font(None, max(14, min(36, sidebar_w // 6)))
            self.title_font.set_bold(True)
        if self.button_font is None:
            self.button_font = g.font.Font(None, max(12, min(28, sidebar_w // 7)))
        
        grid_mid_y = self.offset_y + self.grid_height // 2
        
        title_text = self.title_font.render("MINESWEEPER", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(cx, self.offset_y + 20))
        self.screen.blit(title_text, title_rect)
        
        flag_count = self.model.get_flag_count()
        flag_text = self.button_font.render(f"Flags: {flag_count}/{self.model.num_mines}", True, TEXT_COLOR)
        flag_rect = flag_text.get_rect(center=(cx, grid_mid_y - 20))
        self.screen.blit(flag_text, flag_rect)
        
        elapsed = self.model.get_elapsed_time()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        centiseconds = int((elapsed * 100) % 100)
        timer_text = self.button_font.render(f"Time: {minutes:02d}:{seconds:02d}.{centiseconds:02d}", True, TEXT_COLOR)
        timer_rect = timer_text.get_rect(center=(cx, grid_mid_y + 25))
        self.screen.blit(timer_text, timer_rect)
    
    def draw_game_over_ui(self):
        """Draw the game over UI in the sidebar and store button rects."""
        sidebar_start = self.offset_x + self.grid_width + PADDING
        sidebar_w = max(1, self.screen_width - sidebar_start - PADDING)
        cx = sidebar_start + sidebar_w // 2
        
        if self.title_font is None:
            self.title_font = g.font.Font(None, max(14, min(48, sidebar_w // 5)))
            self.title_font.set_bold(True)
        if self.button_font is None:
            self.button_font = g.font.Font(None, max(12, min(32, sidebar_w // 7)))
        
        grid_mid_y = self.offset_y + self.grid_height // 2
        
        if self.model.game_won:
            status_text = self.title_font.render("YOU WIN!", True, (50, 200, 50))
        else:
            status_text = self.title_font.render("GAME OVER", True, (220, 50, 50))
        status_rect = status_text.get_rect(center=(cx, grid_mid_y - 70))
        self.screen.blit(status_text, status_rect)
        
        elapsed = self.model.get_elapsed_time()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        centiseconds = int((elapsed * 100) % 100)
        timer_text = self.button_font.render(f"Time: {minutes:02d}:{seconds:02d}.{centiseconds:02d}", True, TEXT_COLOR)
        timer_rect = timer_text.get_rect(center=(cx, grid_mid_y))
        self.screen.blit(timer_text, timer_rect)
        
        button_width = min(180, sidebar_w - PADDING)
        button_height = max(35, min(50, self.screen_height // 14))
        button_x = cx - button_width // 2
        restart_button_y = grid_mid_y + 50
        exit_button_y = restart_button_y + button_height + 15
        
        mouse_pos = g.mouse.get_pos()
        restart_hover = button_x <= mouse_pos[0] <= button_x + button_width and restart_button_y <= mouse_pos[1] <= restart_button_y + button_height
        exit_hover = button_x <= mouse_pos[0] <= button_x + button_width and exit_button_y <= mouse_pos[1] <= exit_button_y + button_height
        
        g.draw.rect(self.screen, BUTTON_HOVER_COLOR if restart_hover else BUTTON_COLOR, (button_x, restart_button_y, button_width, button_height), border_radius=8)
        g.draw.rect(self.screen, BUTTON_HOVER_COLOR if exit_hover else BUTTON_COLOR, (button_x, exit_button_y, button_width, button_height), border_radius=8)
        
        restart_text = self.button_font.render("Restart", True, BUTTON_TEXT_COLOR)
        exit_text = self.button_font.render("Exit", True, BUTTON_TEXT_COLOR)
        self.screen.blit(restart_text, restart_text.get_rect(center=(button_x + button_width // 2, restart_button_y + button_height // 2)))
        self.screen.blit(exit_text, exit_text.get_rect(center=(button_x + button_width // 2, exit_button_y + button_height // 2)))
        
        self.restart_rect = (button_x, restart_button_y, button_width, button_height)
        self.exit_rect = (button_x, exit_button_y, button_width, button_height)
    
    def render(self, controller=None):
        """Render the game view, including grid and UI elements."""
        self.screen.fill(BACKGROUND_COLOR)
        
        if controller and controller.is_peek_active() and controller.peek_cell:
            row, col = controller.peek_cell
            self.peek_neighbors = self.model.get_neighbors(row, col)
        else:
            self.peek_neighbors = None
        
        if self.model.game_over:
            self.draw_game_over_grid()
            self.draw_game_over_ui()
        else:
            self.draw_grid()
