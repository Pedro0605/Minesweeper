import numpy as np
from scipy.signal import convolve2d

class GameModel:
    def __init__(self, board_shape=(8, 8), num_mines=10):
        """Initialize the game model with board dimensions and mine count."""
        self.board_shape = board_shape
        self.num_mines = num_mines
        self.kernel = np.array([[1, 1, 1],
                                [1, 1, 1],
                                [1, 1, 1]])
        
        self.mine_board = None
        self.board = None
        self.user_board = None
        self.flag_board = None
        self.game_over = False
        
        self.generate_board()
    
    def generate_board(self):
        """Generate a new game board with randomly placed mines."""
        self.mine_board = np.zeros(shape=self.board_shape)
        mine_positions = np.random.choice(self.mine_board.size, self.num_mines, replace=False)
        self.mine_board.flat[mine_positions] = -1
        
        mines_only = (self.mine_board == -1).astype(int)
        neighbour_count = convolve2d(mines_only, self.kernel, mode='same', boundary='fill')
        neighbour_count -= mines_only
        
        self.board = np.where(self.mine_board == -1, -1, neighbour_count)
        self.user_board = np.full(self.board_shape, -2, dtype=int)
        self.flag_board = np.zeros(self.board_shape, dtype=bool)
        self.game_over = False
    
    def reveal_cell(self, row, col):
        """Reveal a cell at the given position."""
        if 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]:
            if self.user_board[row, col] == -2 and not self.flag_board[row, col]:
                self.user_board[row, col] = self.board[row, col]
                if self.board[row, col] == -1:
                    self.game_over = True
                return True
        return False
    
    def toggle_flag(self, row, col):
        """Toggle flag on a cell at the given position."""
        if 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]:
            if self.user_board[row, col] == -2:
                self.flag_board[row, col] = not self.flag_board[row, col]
                return True
        return False
    
    def get_neighbors(self, row, col):
        """Get the 8 neighboring cells for a given cell."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.board_shape[0] and 0 <= nc < self.board_shape[1]:
                    neighbors.append((nr, nc))
        return neighbors
    
    def chord_cell(self, row, col):
        """Reveal all non-flagged neighbors if flag count matches cell value."""
        if 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]:
            cell_value = self.user_board[row, col]
            
            if cell_value > 0:
                neighbors = self.get_neighbors(row, col)
                flag_count = sum(1 for nr, nc in neighbors if self.flag_board[nr, nc])
                
                if flag_count == cell_value:
                    for nr, nc in neighbors:
                        if not self.flag_board[nr, nc]:
                            self.reveal_cell(nr, nc)
    
    def restart(self):
        """Restart the game by generating a new board."""
        self.generate_board()
