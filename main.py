import pygame as g
from model import GameModel
from view import GameView
from controller import GameController

def main():
    """Initialize and run the Minesweeper game."""
    g.init()
    
    model = GameModel(board_shape=(8, 8), num_mines=10)
    
    screen_width = model.board_shape[1] * 80 + 250 + 40 * 2
    screen_height = max(model.board_shape[0] * 80 + 40 * 2, 500)
    screen = g.display.set_mode((screen_width, screen_height))
    
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
