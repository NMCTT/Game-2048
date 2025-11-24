import pygame
import os
from game.settings import SCREEN
from game.scenes.asset import IMAGE_SCALED_BACKGROUND

class IntroScene:
    def __init__(self):

        self.menu_items = ["PLAYER MODE", "AI MODE", "EXIT"]
        self.total_menu_items = len(self.menu_items)
        self.current_menu_index = 0
        
        self.color_normal = (255, 255, 255)
        self.color_choose = (0, 255, 255)
        self.color_border = (0, 0, 0)
        self.color_border_choose = (0, 0, 255)
        self.outline1 = 5

        self.defaut_font = pygame.font.Font(pygame.font.get_default_font(), 100)

    def Handle_Event(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w):
                self.current_menu_index = self.total_menu_items - 1 if (self.current_menu_index == 0) else self.current_menu_index - 1
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                self.current_menu_index = 0 if (self.current_menu_index == self.total_menu_items - 1) else self.current_menu_index + 1
            if (event.key == pygame.K_RETURN):
                selected_choice = self.menu_items[self.current_menu_index]
                if (selected_choice == "PLAYER MODE"):
                    return "PLAYER MODE"
                if (selected_choice == "AI MODE"):
                    return "AI MODE"
                if (selected_choice == "EXIT"):
                    return "EXIT DIALOG"

    def Draw(self):
        SCREEN.blit(IMAGE_SCALED_BACKGROUND, (0,0))

        #Draw Menu Section
        start_x_position = SCREEN.get_width() / 2
        start_y_position = (SCREEN.get_height() / 2) + 25

        for index in range(0, self.total_menu_items, 1):
            if (index == self.current_menu_index):
                color = self.color_choose
                border = self.color_border_choose
            else:
                color = self.color_normal
                border = self.color_border
            
            current_y_position = start_y_position + index * 130

            (text_surface, border_surface) = self.Create_Text_Border_Surface(
                self.defaut_font, self.menu_items[index], color, border
            )

            text_rect = text_surface.get_rect(center=(start_x_position, current_y_position))

            (Lborder_rect, Tborder_rect, Rborder_rect, Bborder_rect) = self.Create_Border_Rect(
                border_surface, start_x_position, current_y_position, self.outline1
            )

            self.Blit_Text_Border(
                text_surface, border_surface, Lborder_rect, Tborder_rect,
                Rborder_rect, Bborder_rect, text_rect
            )
    
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
    