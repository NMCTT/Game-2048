import pygame
import os
from game.settings import SCREEN
from game.scenes.asset import IMAGE_SCALED_GAME_BG, IMAGE_SCALED_LOGO, IMAGE_SCALED_SCORE

class GameScene:
    def __init__(self):
        self.board_size = 700     
        self.cell_size = 150
        self.padding = 20   

        self.scores = ["0", "1024"]

        self.board_color = (244,240,214)
        self.cell_color = (210,138,96)
        self.BLACK = (0, 0, 0)
        self.DARK_BROWN = (74,48,36)

        self.normalText = pygame.font.Font(pygame.font.get_default_font(), 80)
        self.number = pygame.font.Font(pygame.font.get_default_font(), 30)

    def Handle_Event(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_b): 
                return "BACK TO MENU"

    def Draw(self):
        SCREEN.blit(IMAGE_SCALED_GAME_BG, (0, 0))

        board_x_position = 100
        board_y_position = (SCREEN.get_height() - self.board_size) / 2
        logo_x_position = (SCREEN.get_width() - board_x_position - 470)
        logo_y_position = board_y_position - 125
        boxes_x_position = logo_x_position
        boxes_y_position = logo_y_position + 225

        SCREEN.blit(IMAGE_SCALED_LOGO, (logo_x_position, logo_y_position))
        SCREEN.blit(IMAGE_SCALED_SCORE, (boxes_x_position, boxes_y_position))

        board_rect = pygame.Rect(board_x_position, board_y_position, self.board_size, self.board_size)
        pygame.draw.rect(SCREEN, self.board_color, board_rect, border_radius = 10)

        cell_size_with_padding = self.cell_size + self.padding
        for i in range(0, 4, 1):
            for j in range(0, 4, 1):
                cell_x_position = board_x_position + self.padding + j * cell_size_with_padding
                cell_y_position = board_y_position + self.padding + i * cell_size_with_padding
                cell_rect = pygame.Rect(cell_x_position, cell_y_position, self.cell_size, self.cell_size)
                pygame.draw.rect(SCREEN, self.cell_color, cell_rect, border_radius = 10)

        for i in range(0, 2, 1):
            (score_surface, border_surface) = self.Create_Text_Border_Surface(
                self.number, self.scores[i], self.DARK_BROWN, self.BLACK
            )
            center_x = boxes_x_position + 140 + i * 227
            center_y = boxes_y_position + 160
            score_rect = score_surface.get_rect(center=(center_x, center_y)) 
            (left, top, right, bottom) = self.Create_Border_Rect(border_surface, center_x, center_y, 2)
            self.Blit_Text_Border(score_surface, border_surface, left, top, right, bottom, score_rect)



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
