import pygame as g
from view import CELL_SIZE, SIDEBAR_WIDTH, PADDING

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
    
    def handle_cell_click(self, mouse_x, mouse_y):
        col = (mouse_x - self.view.offset_x) // CELL_SIZE
        row = (mouse_y - self.view.offset_y) // CELL_SIZE
        self.model.reveal_cell(row, col)
    
    def handle_cell_right_click(self, mouse_x, mouse_y):
        col = (mouse_x - self.view.offset_x) // CELL_SIZE
        row = (mouse_y - self.view.offset_y) // CELL_SIZE
        self.model.toggle_flag(row, col)
    
    def handle_button_click(self, mouse_x, mouse_y, restart_rect, exit_rect):
        if restart_rect[0] <= mouse_x <= restart_rect[0] + restart_rect[2] and restart_rect[1] <= mouse_y <= restart_rect[1] + restart_rect[3]:
            self.model.restart()
        elif exit_rect[0] <= mouse_x <= exit_rect[0] + exit_rect[2] and exit_rect[1] <= mouse_y <= exit_rect[1] + exit_rect[3]:
            self.running = False
    
    def process_events(self):
        for event in g.event.get():
            if event.type == g.QUIT:
                self.running = False
            elif event.type == g.MOUSEBUTTONDOWN:
                if self.model.game_over:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        sidebar_x = self.view.offset_x + self.view.grid_width + 30
                        button_width = 180
                        button_height = 50
                        button_x = sidebar_x + (SIDEBAR_WIDTH - 30 - button_width) // 2
                        restart_button_y = self.view.screen_height - 150
                        exit_button_y = self.view.screen_height - 80
                        restart_rect = (button_x, restart_button_y, button_width, button_height)
                        exit_rect = (button_x, exit_button_y, button_width, button_height)
                        self.handle_button_click(mouse_x, mouse_y, restart_rect, exit_rect)
                else:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        self.handle_cell_click(mouse_x, mouse_y)
                    elif event.button == 3:
                        mouse_x, mouse_y = event.pos
                        self.handle_cell_right_click(mouse_x, mouse_y)
