import pygame
import game.logic as logic 
from game.settings import SCREEN
from game.scenes.asset import IMAGE_SCALED_GAME_BG, IMAGE_SCALED_LOGO, IMAGE_SCALED_SCORE
from game.scenes.asset import E9_ANIMATION, WALK_ANIMATION, LOSE_ANIMATION
from game.scenes.tile import Tile

BOARD_BACK_MENU = "BACK TO MENU"
BOARD_LEFT = "LEFT"
BOARD_RIGHT = "RIGHT"
BOARD_UP = "UP"
BOARD_DOWN = "DOWN"
BOARD_BEST_SCORE = "200"
BOARD_GAME_OVER = "GAME OVER"

class GameScene:
    def __init__(self):
        self.board_size = 700     
        self.cell_size = 150
        self.padding = 20   

        self.frames = [E9_ANIMATION, WALK_ANIMATION, LOSE_ANIMATION]
        self.current_frame = [0, 0, 0]
        self.animation_best = self.frames[0][self.current_frame[0]]
        self.animation_walk = self.frames[1][self.current_frame[1]]
        self.animation_lose = self.frames[2][self.current_frame[2]]
        self.animation_speed = 100
        self.last_animation_time = pygame.time.get_ticks()

        self.scores = ["0", BOARD_BEST_SCORE]
        self.old_best_score = BOARD_BEST_SCORE

        self.board_color = (244,240,214)
        self.cell_color = (210,138,96)
        self.BLACK = (0, 0, 0)
        self.DARK_BROWN = (74,48,36)
        self.PURPLE = (175, 60, 185)
        self.PURPLE_BG = (75, 45, 85)

        self.normalText = pygame.font.Font(pygame.font.get_default_font(), 80)
        self.number = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.cellNumber = pygame.font.Font(pygame.font.get_default_font(), 60)

        self.board_x_position = 100
        self.board_y_position = (SCREEN.get_height() - self.board_size) / 2
        self.logo_x_position = SCREEN.get_width() - self.board_x_position - 470
        self.logo_y_position = self.board_y_position - 125
        self.boxes_x_position = self.logo_x_position
        self.boxes_y_position = self.logo_y_position + 225

        self.bar_x_position = self.logo_x_position + 50
        self.bar_y_position = (SCREEN.get_height() / 2) + 100
        self.bar_width = 400
        self.bar_height = 20

        self.board_rect = pygame.Rect(
            self.board_x_position, self.board_y_position, self.board_size, self.board_size
        )
        self.bar_rect = pygame.Rect(
            self.bar_x_position, self.bar_y_position, self.bar_width, self.bar_height
        )
        
        self.tiles = []
        logic.start_game()
        # Lần đầu chạy không có hướng
        self.sync_tiles_from_logic() 

    def sync_tiles_from_logic(self, direction=None): 
        new_tiles_list = []
        old_tiles_pool = self.tiles[:] 
        cell_size_with_padding = self.cell_size + self.padding

        for i in range(4):
            for j in range(4):
                value = logic.g_board[i][j]
                if value != 0:
                    target_x = self.board_x_position + self.padding + j * cell_size_with_padding
                    target_y = self.board_y_position + self.padding + i * cell_size_with_padding

                    found_tile = None
                    shortest_distance = 1000000

                    for tile in old_tiles_pool:
                        if tile.value == value:
                            distance = (tile.x - target_x)**2 + (tile.y - target_y)**2
                            
                            # === [FIX] LUẬT ===
                            is_valid_path = False
                            
                            if direction == BOARD_LEFT:
                                # 1. Phải cùng hàng (Row)
                                # 2. Cấm đi lùi (X cũ phải nằm bên phải đích đến)
                                if tile.row == i and tile.x >= target_x: 
                                    is_valid_path = True
                                    
                            elif direction == BOARD_RIGHT:
                                # X cũ phải nằm bên trái đích đến
                                if tile.row == i and tile.x <= target_x: 
                                    is_valid_path = True
                                    
                            elif direction == BOARD_UP:
                                # 1. Phải cùng cột (Col)
                                # 2. Cấm đi lùi (Y cũ phải nằm dưới đích đến)
                                if tile.col == j and tile.y >= target_y: 
                                    is_valid_path = True
                                    
                            elif direction == BOARD_DOWN:
                                # Y cũ phải nằm trên đích đến
                                if tile.col == j and tile.y <= target_y: 
                                    is_valid_path = True
                                    
                            else:
                                is_valid_path = True # Không có hướng (lúc mới vào game)
                            # ===========================================

                            if is_valid_path and distance < shortest_distance:
                                shortest_distance = distance
                                found_tile = tile
                    
                    if found_tile:
                        found_tile.row = i
                        found_tile.col = j
                        found_tile.target_x = target_x
                        found_tile.target_y = target_y
                        new_tiles_list.append(found_tile)
                        old_tiles_pool.remove(found_tile)
                    else:
                        new_tile = Tile(value, i, j, target_x, target_y, self.cell_size, self.cellNumber)
                        new_tile.scale = 0
                        new_tiles_list.append(new_tile)
        
        self.tiles = new_tiles_list

    def Handle_Event(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_b): 
                return BOARD_BACK_MENU
            
            direction = None
            if (event.key == pygame.K_w or event.key == pygame.K_UP):
                direction = BOARD_UP
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN):
                direction = BOARD_DOWN
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                direction = BOARD_LEFT
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                direction = BOARD_RIGHT
            
            if direction != None:
                # 1. Gọi Logic
                result = logic.Handle_Event(direction)
                # 2. Đồng bộ hình ảnh ngay lập tức
                self.sync_tiles_from_logic(direction)
                
                if result == BOARD_GAME_OVER:
                    return BOARD_BACK_MENU

    def Draw(self):
        # Vẽ nền
        SCREEN.blit(IMAGE_SCALED_GAME_BG, (0, 0))
        SCREEN.blit(IMAGE_SCALED_LOGO, (self.logo_x_position, self.logo_y_position))
        SCREEN.blit(IMAGE_SCALED_SCORE, (self.boxes_x_position, self.boxes_y_position))

        pygame.draw.rect(SCREEN, self.board_color, self.board_rect, border_radius = 10)

        cell_size_with_padding = self.cell_size + self.padding

        # Vẽ các ô trống (nền dưới gạch)
        for i in range(4):
            for j in range(4):
                cell_x_position = self.board_x_position + self.padding + j * cell_size_with_padding
                cell_y_position = self.board_y_position + self.padding + i * cell_size_with_padding
                cell_rect = pygame.Rect(cell_x_position, cell_y_position, self.cell_size, self.cell_size)
                pygame.draw.rect(SCREEN, self.cell_color, cell_rect, border_radius = 10)
        
        # VẼ CÁC VIÊN GẠCH (QUAN TRỌNG NHẤT)
        for tile in self.tiles:
            tile.update_position() # <--- Di chuyển gạch từng chút một
            tile.draw(SCREEN)      # <--- Vẽ lên màn hình

        # Vẽ điểm số
        self.scores[0] = str(logic.g_score)
        if (self.scores[0] == "0"):
            self.old_best_score = self.scores[1]
        if (int(self.scores[1]) < logic.g_score):
            self.scores[1] = str(logic.g_score)

        for i in range(0, 2, 1):
            (score_surface, border_surface) = self.Create_Text_Border_Surface(
                self.number, self.scores[i], self.DARK_BROWN, self.BLACK
            )
            center_x = self.boxes_x_position + 140 + i * 227
            center_y = self.boxes_y_position + 160
            score_rect = score_surface.get_rect(center=(center_x, center_y)) 
            (left, top, right, bottom) = self.Create_Border_Rect(border_surface, center_x, center_y, 2)
            self.Blit_Text_Border(score_surface, border_surface, left, top, right, bottom, score_rect)
        
        self.Draw_Score_Bar()

    def Draw_Score_Bar(self):
        self.Update_Animation()

        current_score = int(self.scores[0])
        best_score = int(self.old_best_score)

        if current_score > best_score:
            limit = current_score * 1.1

        else:
            limit = best_score
        
        player_x_position = self.bar_x_position + (self.bar_width * (current_score / limit))
        best_x_position = self.bar_x_position + (self.bar_width * (best_score / limit))

        process_width = player_x_position - self.bar_x_position
        process_rect = pygame.Rect(
            self.bar_x_position, self.bar_y_position, process_width, self.bar_height
        )

        pygame.draw.rect(SCREEN, self.PURPLE_BG, self.bar_rect, border_radius = 3)
        if (process_width > 0):
            pygame.draw.rect(SCREEN, self.PURPLE, process_rect, border_radius = 3)
        
        best_rect = self.animation_best.get_rect(center=(best_x_position - 5, self.bar_y_position - 60))
        player_rect = self.animation_walk.get_rect(center=(player_x_position, self.bar_y_position - 60))

        SCREEN.blit(self.animation_best, best_rect)
        SCREEN.blit(self.animation_walk, player_rect)

    def Update_Animation(self):
        current_time = pygame.time.get_ticks()
        passed_time = current_time - self.last_animation_time

        if (passed_time > self.animation_speed):
            self.last_animation_time = current_time

            for i in range(0, len(self.frames), 1):
                next_frame = self.current_frame[i] + 1
                self.current_frame[i] = next_frame if (next_frame < len(self.frames[i])) else 0
        
            index = 2 if (int(self.scores[0]) > int(self.old_best_score)) else 0

            self.animation_best = self.frames[index][self.current_frame[index]]
            self.animation_walk = self.frames[1][self.current_frame[1]]

    def Blit_Text_Border(self, text_surface, border_surface, left, top, right, bottom, rect):
        SCREEN.blit(border_surface, left)
        SCREEN.blit(border_surface, top)
        SCREEN.blit(border_surface, right)
        SCREEN.blit(border_surface, bottom)
        SCREEN.blit(text_surface, rect)
    
    def Create_Border_Rect(self, surface, center_x, center_y, outline):
        Left_Rect = surface.get_rect(center=(center_x - outline, center_y))
        Top_Rect = surface.get_rect(center=(center_x, center_y - outline))
        Right_Rect = surface.get_rect(center=(center_x + outline, center_y))
        Bottom_Rect = surface.get_rect(center=(center_x, center_y + outline))
        return (Left_Rect, Top_Rect, Right_Rect, Bottom_Rect)

    def Create_Text_Border_Surface(self, font, text, text_color, border_color):
        text_surface = font.render(text, True, text_color)
        border_surface = font.render(text, True, border_color)
        return (text_surface, border_surface)