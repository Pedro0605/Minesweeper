import pygame as g
from view import PADDING, SIDEBAR_WIDTH

PEEK_THRESHOLD_MS = 200

class GameController:
    def __init__(self, model, view):
        """Initialize the game controller."""
        self.model = model
        self.view = view
        self.running = True
        self.peeking = False
        self.peek_cell = None
        self.mouse_down_time = 0
    
    def is_peek_active(self):
        """Check if peek highlighting should be active based on elapsed time."""
        if not self.peeking or self.mouse_down_time == 0:
            return False
        elapsed = g.time.get_ticks() - self.mouse_down_time
        return elapsed >= PEEK_THRESHOLD_MS
    
    def handle_cell_click(self, mouse_x, mouse_y):
        """Handle left click on a cell to reveal it or chord."""
        cs = self.view.cell_size
        col = (mouse_x - self.view.offset_x) // cs
        row = (mouse_y - self.view.offset_y) // cs
        
        if 0 <= row < self.model.board_shape[0] and 0 <= col < self.model.board_shape[1]:
            if self.model.user_board[row, col] > 0:
                self.model.chord_cell(row, col)
            else:
                self.model.reveal_cell(row, col)
    
    def handle_cell_right_click(self, mouse_x, mouse_y):
        """Handle right click on a cell to toggle flag."""
        cs = self.view.cell_size
        col = (mouse_x - self.view.offset_x) // cs
        row = (mouse_y - self.view.offset_y) // cs
        self.model.toggle_flag(row, col)
    
    def handle_button_click(self, mouse_x, mouse_y, restart_rect, exit_rect):
        """Handle clicks on restart and exit buttons."""
        if restart_rect[0] <= mouse_x <= restart_rect[0] + restart_rect[2] and restart_rect[1] <= mouse_y <= restart_rect[1] + restart_rect[3]:
            self.model.restart()
        elif exit_rect[0] <= mouse_x <= exit_rect[0] + exit_rect[2] and exit_rect[1] <= mouse_y <= exit_rect[1] + exit_rect[3]:
            self.running = False
    
    def process_events(self):
        """Process pygame events including mouse clicks and window events."""
        for event in g.event.get():
            if event.type == g.QUIT:
                self.running = False
            elif event.type == g.VIDEORESIZE:
                # pygame 1 fallback: only needed if not on SDL2
                w, h = event.w, event.h
                self.view.update_dimensions(w, h)
            elif event.type == g.WINDOWRESIZED:
                # pygame 2 / SDL2: surface already resized, just update layout
                w, h = self.view.screen.get_size()
                self.view.update_dimensions(w, h)
            elif event.type == g.MOUSEBUTTONDOWN:
                if self.model.game_over:
                    if event.button == 1 and self.view.restart_rect and self.view.exit_rect:
                        mouse_x, mouse_y = event.pos
                        self.handle_button_click(mouse_x, mouse_y, self.view.restart_rect, self.view.exit_rect)
                else:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        col = (mouse_x - self.view.offset_x) // self.view.cell_size
                        row = (mouse_y - self.view.offset_y) // self.view.cell_size
                        if 0 <= row < self.model.board_shape[0] and 0 <= col < self.model.board_shape[1]:
                            self.peeking = True
                            self.peek_cell = (row, col)
                            self.mouse_down_time = g.time.get_ticks()
                    elif event.button == 3:
                        mouse_x, mouse_y = event.pos
                        self.handle_cell_right_click(mouse_x, mouse_y)
            elif event.type == g.MOUSEBUTTONUP:
                if event.button == 1 and not self.model.game_over:
                    mouse_up_time = g.time.get_ticks()
                    click_duration = mouse_up_time - self.mouse_down_time
                    
                    if click_duration < PEEK_THRESHOLD_MS and self.peek_cell:
                        mouse_x, mouse_y = event.pos
                        self.handle_cell_click(mouse_x, mouse_y)
                    
                    self.peeking = False
                    self.peek_cell = None
                    self.mouse_down_time = 0
