import numpy as np
from game.logic import (
    move_board_left,
    move_board_right,
    transpose,
    spawn_tile,
    can_move
)

class Game2048Env:
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.reset()

    def reset(self):
        self.board[:] = 0
        spawn_tile(self.board)
        spawn_tile(self.board)
        self.score = 0
        return self.board.copy()
    
    def step(self, action):
        old_board = self.board.copy()

        # ---- Hành động ----
        if action == 2:  # LEFT
            reward_step = move_board_left(self.board)
        elif action == 3:  # RIGHT
            reward_step = move_board_right(self.board)
        elif action == 0:  # UP
            temp = self.board.T.copy()
            reward_step = move_board_left(temp)
            self.board = temp.T.copy()
        elif action == 1:  # DOWN
            temp = self.board.T.copy()
            reward_step = move_board_right(temp)
            self.board = temp.T.copy()
        else:
            raise ValueError("Invalid action")

        # ---- Check movement ----
        moved = not np.array_equal(old_board, self.board)
        if moved:
            spawn_tile(self.board)
            self.score += reward_step
        else:
            reward_step = -1  # penalty move vô ích

        # ---- Game over ----
        done = not can_move(self.board)

        # ---- Tối ưu reward ----
        # reward = log2 của tất cả các ô gộp step hiện tại + penalty
        merged_board = self._calculate_merged(old_board, self.board)
        reward = np.sum(np.log2(merged_board[merged_board>0])) + reward_step

        return self.board.astype(np.float32), reward, done, {}
    
    def _calculate_merged(self, old_board, new_board):
        merged = np.zeros((4,4), dtype=int)
        for i in range(4):
            for j in range(4):
                if new_board[i,j] > old_board[i,j] and old_board[i,j] != 0:
                    merged[i,j] = new_board[i,j] - old_board[i,j]
        return merged
