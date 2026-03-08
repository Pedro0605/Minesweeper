import pygame as g
from model import GameModel
from view import GameView, CELL_SIZE, PADDING, SIDEBAR_WIDTH
from controller import GameController

def main():
    """Initialize and run the Minesweeper game."""
    g.init()
    
    model = GameModel(board_shape=(16, 16), num_mines=40)
    
    grid_width = model.board_shape[1] * CELL_SIZE
    grid_height = model.board_shape[0] * CELL_SIZE
    screen_width = grid_width + SIDEBAR_WIDTH + PADDING * 2
    screen_height = max(grid_height + PADDING * 2, 500)
    
    screen = g.display.set_mode((screen_width, screen_height), g.RESIZABLE)
    g.display.set_caption("Minesweeper")
    
    view = GameView(screen, model)
    controller = GameController(model, view)
    
    clock = g.time.Clock()
    
    while controller.running:
        controller.process_events()
        view.render(controller)
        g.display.flip()
        clock.tick(60)
    
    g.quit()

if __name__ == "__main__":
    main()
