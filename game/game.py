import pygame
import random
import copy
board = [[0 for _ in range(4)] for _ in range(4)]
score = 0
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


def move_row(row, direction="left"):
    if direction == "left":
        new_row, gained = compress_merge(row)
        return new_row,gained
    elif direction == "right":
        reversed_row = row[::-1]
        merged,gained = compress_merge(reversed_row)
        return merged[::-1],gained
        
       
    

def move_board(board,direction = "left"):
   total_gain = 0
   for i in range(4):
      new_row,gained  = move_row(board[i],direction)
      total_gain += gained
      board[i] = new_row
   return total_gain


spawn_tile(board)
spawn_tile(board)
for i in board:
    print(i)
pygame.init()
screen = pygame.display.set_mode((1000, 600))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
           exit()
        if not can_move(board):
           print("GAME OVER")
           pygame.quit()
           exit()
        if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_LEFT:
            board1 = copy.deepcopy(board)
            gain = move_board(board,"left")
            score += gain
            if(board1 != board):
               spawn_tile(board)
            for i in board:
               print(i)
            print(score)
            print()
            print ("------")
         elif event.key == pygame.K_RIGHT:
            board1 = copy.deepcopy(board)
            gain = move_board(board,"right")
            score += gain
            if(board1 != board):
               spawn_tile(board)
            for i in board:
               print(i)
            print(score)
            print()
            print("--------")
         elif event.key == pygame.K_UP:
            board1 = copy.deepcopy(board)
            transposed_board = transpose(board)
            gain = move_board(transposed_board,"left")
            score += gain
            board = transpose(transposed_board)
            if(board1 != board):
               spawn_tile(board)
            for i in board:
               print(i)
            print(score)
            print()
            print("-------")
         elif event.key == pygame.K_DOWN:
            board1 = copy.deepcopy(board)
            transposed_board = transpose(board)
            gain =  move_board(transposed_board,"right")
            score += gain
            board = transpose(transposed_board)
            if(board1 != board):
               spawn_tile(board)
            for i in board:
               print(i)
            print(score)
            print()
            
            print("--------")
