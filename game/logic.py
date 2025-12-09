import random
import copy

g_board = [[0 for _ in range(4)] for _ in range(4)]
g_score = 0
g_is_game_over = False

LOGIC_LEFT = "LEFT"
LOGIC_RIGHT = "RIGHT"
LOGIC_UP = "UP"
LOGIC_DOWN = "DOWN"

LOGIC_MOVED = True
LOGIC_UNMOVED = False
LOGIC_GAME_OVER = "GAME OVER"

def Handle_Event(direction):
   global g_board, g_score, g_is_game_over

   board_backup = copy.deepcopy(g_board)
   gain = 0

   if direction == LOGIC_LEFT:
      gain = move_board_left(g_board)
   elif direction == LOGIC_RIGHT:
      gain = move_board_right(g_board)
   elif direction == LOGIC_UP:
      g_board = transpose(g_board)
      gain = move_board_left(g_board)
      g_board = transpose(g_board)
   elif direction == LOGIC_DOWN:
      g_board = transpose(g_board)
      gain = move_board_right(g_board)
      g_board = transpose(g_board)

   if board_backup != g_board:
      g_score += gain
      spawn_tile(g_board)

      if not can_move(g_board):
         g_is_game_over = True
         return LOGIC_GAME_OVER

      return LOGIC_MOVED
   
   if not can_move(g_board):
      g_is_game_over = True
      return LOGIC_GAME_OVER

   return LOGIC_UNMOVED

def reset_board(board):
    for row in range(4):
        for column in range(4):
            board[row][column] = 0

def get_empty_cells(board):
    return [(row, column) for row in range(4) for column in range(4) if board[row][column] == 0]
   
def start_game():
   global g_board, g_score, g_is_game_over
   reset_board(g_board)
   g_score = 0
   g_is_game_over = False

   spawn_tile(g_board)
   spawn_tile(g_board)

def spawn_tile(board):
    empty_cells = get_empty_cells(board)

    if not empty_cells:
        return

    (row, column) = random.choice(empty_cells)
    board[row][column] = 4 if random.random() < 0.1 else 2

def can_move(board):
    for row in board:
        if 0 in row:
            return True
    
    for i in range(4):
        for j in range(4):
            if j - 1 >= 0:
                if board[i][j] == board[i][j - 1]:
                    return True
            if i - 1 >= 0:
                if board[i][j] == board[i - 1][j]:
                    return True
            if i + 1 <= 3:
                if board[i][j] == board[i + 1][j]:
                    return True
            if j + 1 <= 3:
                if board[i][j] == board[i][j + 1]:
                    return True
    return False

def transpose(board):
   return [list(row) for row in zip(*board)]

def compress_merge(row):
    cell_idx = 0
    score_gained = 0
    new_row = [cell for cell in row if cell != 0]

    while cell_idx < len(new_row)-1:
        if new_row[cell_idx] != new_row[cell_idx+1]:
            cell_idx += 1
            continue

        new_row[cell_idx] *= 2
        score_gained += new_row[cell_idx]
        new_row[cell_idx+1] = 0
        cell_idx += 2

    new_row = [cell for cell in new_row if cell != 0]

    while len(new_row) < 4:
        new_row.append(0)

    return new_row, score_gained

def move_row_left(row):
    return compress_merge(row)

def move_row_right(row):
    reversed_row = row[::-1]
    (merged, gained) = compress_merge(reversed_row)
    return merged[::-1], gained

def move_board_left(board):
   total_gain = 0

   for row in range(4):
      new_row, gained = move_row_left(board[row])
      total_gain += gained
      board[row] = new_row

   return total_gain

def move_board_right(board):
    total_gain = 0

    for row in range(4):
        new_row, gained = move_row_right(board[row])
        total_gain += gained
        board[row] = new_row

    return total_gain


