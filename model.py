import numpy as np
from scipy.signal import convolve2d

class GameModel:
    def __init__(self, board_shape=(8, 8), num_mines=10):
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
        if 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]:
            if self.user_board[row, col] == -2 and not self.flag_board[row, col]:
                self.user_board[row, col] = self.board[row, col]
                if self.board[row, col] == -1:
                    self.game_over = True
                return True
        return False
    
    def toggle_flag(self, row, col):
        if 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]:
            if self.user_board[row, col] == -2:
                self.flag_board[row, col] = not self.flag_board[row, col]
                return True
        return False
    
    def restart(self):
        self.generate_board()
