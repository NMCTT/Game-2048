import random
import copy

board = [[0 for _ in range(4)] for _ in range(4)]
score = 0
is_game_over = False

LOGIC_LEFT = "LEFT"
LOGIC_RIGHT = "RIGHT"
LOGIC_UP = "UP"
LOGIC_DOWN = "DOWN"

LOGIC_MOVED = True
LOGIC_UNMOVED = False
LOGIC_GAME_OVER = "GAME OVER"

def Handle_Event(direction):
   global board, score, is_game_over

   board_backup = copy.deepcopy(board)
   gain = 0

   if direction == LOGIC_LEFT:
      gain = move_board(board, LOGIC_LEFT)
   elif direction == LOGIC_RIGHT:
      gain = move_board(board, LOGIC_RIGHT)
   elif direction == LOGIC_UP:
      board = transpose(board)
      gain = move_board(board, LOGIC_LEFT)
      board = transpose(board)
   elif direction == LOGIC_DOWN:
      board = transpose(board)
      gain = move_board(board, LOGIC_RIGHT)
      board = transpose(board)

   if board_backup != board:
      score += gain
      spawn_tile(board)

      if not can_move(board):
         is_game_over = True
         return LOGIC_GAME_OVER

      return LOGIC_MOVED
   
   if not can_move(board):
      is_game_over = True
      return LOGIC_GAME_OVER

   return LOGIC_UNMOVED
   
def start_game():
   global board, score, is_game_over
   board = [[0 for _ in range(4)] for _ in range(4)]
   score = 0
   is_game_over = False;
   spawn_tile(board)
   spawn_tile(board)
   return board 

def spawn_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty_cells:
        return
    i,j = random.choice(empty_cells) 
    board[i][j] = 4 if random.random() < 0.1 else 2

def can_move(board):
   for row in board:
        if 0 in row:
            return True
   for i in range(4):
        for j in range(4):
            if j < 3 and board[i][j] == board[i][j+1]:
                return True
            if i < 3 and board[i][j] == board[i+1][j]:
                return True
   return False

def transpose(board):
   return [list(row) for row in zip(*board)]

def compress_merge(row):
   new_row = [i for i in row if i != 0]
   i = 0
   score_gain = 0
   while i < len(new_row) -1:
      if new_row[i] == new_row[i+1]:
         new_row[i] *= 2
         score_gain += new_row[i]
         new_row[i+1] = 0
         i+= 2
      else: i+=1
   new_row = [i for i in new_row if i != 0]
   while len(new_row) < 4 :
      new_row.append(0)
   return new_row,score_gain

def move_row(row, direction):
    if direction == LOGIC_LEFT:
        new_row, gained = compress_merge(row)
        return new_row,gained
    elif direction == LOGIC_RIGHT:
        reversed_row = row[::-1]
        merged,gained = compress_merge(reversed_row)
        return merged[::-1],gained
        
def move_board(board, direction):
   total_gain = 0
   for i in range(4):
      new_row,gained  = move_row(board[i],direction)
      total_gain += gained
      board[i] = new_row
   return total_gain


