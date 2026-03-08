import numpy as np
from scipy.signal import convolve2d
import time

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
        self.game_won = False
        self.game_started = False
        self.start_time = None
        self.final_time = 0
        
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
        self.game_won = False
        self.game_started = False
        self.start_time = None
        self.final_time = 0
    
    def reveal_cell(self, row, col):
        """Reveal a cell at the given position."""
        if 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]:
            if self.user_board[row, col] == -2 and not self.flag_board[row, col]:
                if not self.game_started:
                    self.game_started = True
                    self.start_time = time.time()
                
                self.user_board[row, col] = self.board[row, col]
                if self.board[row, col] == -1:
                    self.game_over = True
                    if self.start_time is not None:
                        self.final_time = time.time() - self.start_time
                elif self.board[row, col] == 0:
                    self.flood_fill(row, col)
                
                self.check_win()
                return True
        return False
    
    def flood_fill(self, row, col):
        """Recursively reveal all connected empty cells and their numbered borders."""
        neighbors = self.get_neighbors(row, col)
        
        for nr, nc in neighbors:
            if self.user_board[nr, nc] == -2 and not self.flag_board[nr, nc]:
                self.user_board[nr, nc] = self.board[nr, nc]
                
                if self.board[nr, nc] == 0:
                    self.flood_fill(nr, nc)
    
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
    
    def check_win(self):
        """Check if the player has won by revealing all non-mine cells."""
        if not self.game_over:
            unrevealed_count = np.sum(self.user_board == -2)
            if unrevealed_count == self.num_mines:
                self.game_won = True
                self.game_over = True
                if self.start_time is not None:
                    self.final_time = time.time() - self.start_time
    
    def get_flag_count(self):
        """Get the number of flags currently placed."""
        return np.sum(self.flag_board)
    
    def get_elapsed_time(self):
        """Get the elapsed time since the game started."""
        if not self.game_started or self.start_time is None:
            return 0
        if self.game_over:
            return self.final_time
        return time.time() - self.start_time
    
    def restart(self):
        """Restart the game by generating a new board."""
        self.generate_board()
