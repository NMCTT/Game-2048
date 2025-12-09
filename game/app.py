import pygame
from sys import exit
import game.logic as logic
# import game.scenes.board as board
from game.settings import SCREEN, CLOCK
from game.scenes.asset import IMAGE_SCALED_EXIT_GAME, IMAGE_SCALED_EXIT_BOARD, IMAGE_SCALED_GAME_OVER
from game.scenes.intro import IntroScene
from game.scenes.board import GameScene

APP_QUIT = "QUIT"
APP_PLAYER_MODE = "PLAYER MODE"
APP_AI_MODE = "AI MODE"
APP_BACK_MENU = "BACK TO MENU"
APP_EXIT_DIALOG = "EXIT DIALOG"
APP_GAME_OVER = "GAME_OVER"

class App:
    def __init__(self):
        self.Intro = IntroScene() 
        self.Board = GameScene()
        self.current_scene = self.Intro

        self.dialog_items = ["YES", "NO"]
        self.total_dialog_items = len(self.dialog_items)
        self.current_dialog_index = 1
        self.dialog_confirm = False

        self.game_over_timestamp = 0

        self.color_normal = (255, 255, 255)
        self.color_choose = (0, 255, 255)
        self.color_border = (0, 0, 0)
        self.color_border_choose = (0, 0, 255)
        self.qs_color = (80, 200, 120)
        self.qs_border = (10, 92, 11)
        self.outline2 = 2

        self.dialog_font = pygame.font.Font(pygame.font.get_default_font(), 70)

        self.qs_center_x = SCREEN.get_width() / 2
        self.qs_center_y = (SCREEN.get_height() / 2) - 200
        self.acp_center_x = (SCREEN.get_width() / 2) - 150
        self.deny_center_x = (SCREEN.get_width() / 2) + 150
        self.ans_center_y = (SCREEN.get_height() / 2) + 200


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.dialog_confirm:
                    signal = self.Handle_Dialog_Event(event) 
                    if (signal == APP_QUIT and self.current_scene == self.Intro):
                        running = False
                    elif (signal == APP_QUIT and self.current_scene == self.Board):
                        self.current_scene = self.Intro
                else:
                    signal = self.current_scene.Handle_Event(event)
                    self.Handle_Signal(signal)
            
            if logic.g_is_game_over == False:
                self.game_over_timestamp = 0
            elif logic.g_is_game_over == True and self.game_over_timestamp == 0:
                self.game_over_timestamp = pygame.time.get_ticks()

            self.current_scene.Draw()

            if self.dialog_confirm:
                self.Draw_Exit_Dialog()

            pygame.display.update()
            CLOCK.tick(60)

        pygame.quit()
        exit()

    def Handle_Dialog_Event(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                self.current_dialog_index = 0 if (self.current_dialog_index == 1) else 1
            if (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                self.current_dialog_index = 0 if (self.current_dialog_index == 1) else 1
            if (event.key == pygame.K_RETURN):
                selected_choice = self.dialog_items[self.current_dialog_index]
                if (selected_choice == "YES"):
                    self.dialog_confirm = False
                    if (self.current_scene == self.Board and logic.g_is_game_over == True):
                        logic.start_game()
                        self.Board.tiles.clear()
                        return None
                    return "QUIT"

                if (selected_choice == "NO"):
                    self.dialog_confirm = False
                    if (self.current_scene == self.Board and logic.g_is_game_over == True):
                        logic.start_game()
                        self.Board.tiles.clear()
                        return "QUIT"

    def Handle_Signal(self, signal):
        if signal == APP_PLAYER_MODE:
            self.current_scene = self.Board
        elif signal == APP_BACK_MENU:
            self.dialog_confirm = True
            self.current_dialog_index = 1
        elif signal == APP_GAME_OVER:
            self.dialog_confirm = True
            self.current_dialog_index = 0
        elif signal == APP_AI_MODE:
            self.dialog_confirm = False  # FIx khi lam them scene AI mode
        elif signal == APP_EXIT_DIALOG:
            self.dialog_confirm = True
            self.current_dialog_index = 1

    def Draw_Exit_Dialog(self):
        current_time = pygame.time.get_ticks()
        passed_time = current_time - self.game_over_timestamp

        if (logic.g_is_game_over == True and passed_time < 1500):
            return

        if (self.current_dialog_index == 0):
            acpColor = self.color_choose
            acpBorder = self.color_border_choose
            denyColor = self.color_normal
            denyBorder = self.color_border
        else:
            denyColor = self.color_choose
            denyBorder = self.color_border_choose
            acpColor = self.color_normal
            acpBorder = self.color_border

        layer_surface = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
        layer_surface.fill((0, 0, 0, 150))
        
        SCREEN.blit(layer_surface, (0, 0))

        box_width = 800
        box_height = 600
        box_x_position = (SCREEN.get_width() - box_width) / 2
        box_y_position = (SCREEN.get_height() - box_height) / 2

        dialog_rect = pygame.Rect(box_x_position, box_y_position, box_width, box_height)
        pygame.draw.rect(SCREEN, (87,65,48), dialog_rect, 5)
        pygame.draw.rect(SCREEN, (193,165,124), dialog_rect, 0, 5)
        
        if (self.current_scene == self.Intro):
            question = "CONFIRM TO LEAVE??"
            image = IMAGE_SCALED_EXIT_GAME
        elif (
            self.current_scene == self.Board and logic.g_is_game_over == True):
            question = "WANNA REPLAY??"
            image = IMAGE_SCALED_GAME_OVER
        elif (self.current_scene == self.Board and logic.g_is_game_over == False):
            question = "BACK TO MENU??"
            image = IMAGE_SCALED_EXIT_BOARD

        (text_qs_surface, border_qs_surface) = self.Create_Text_Border_Surface(
            self.dialog_font, question, self.qs_color, self.qs_border
        )
        (acp_surface, border_acp_surface) = self.Create_Text_Border_Surface(
            self.dialog_font, self.dialog_items[0], acpColor, acpBorder
        )
        (deny_surface, border_deny_surface) = self.Create_Text_Border_Surface(
            self.dialog_font, self.dialog_items[1], denyColor, denyBorder
        )

        text_qs_rect = text_qs_surface.get_rect(center=(self.qs_center_x, self.qs_center_y))
        acp_rect = acp_surface.get_rect(center=(self.acp_center_x, self.ans_center_y))
        deny_rect = deny_surface.get_rect(center=(self.deny_center_x, self.ans_center_y))

        (Lborder_qs_rect, Tborder_qs_rect, Rborder_qs_rect, Bborder_qs_rect) = self.Create_Border_Rect(
            border_qs_surface, self.qs_center_x, self.qs_center_y, self.outline2
        )

        (Lborder_acp_rect, Tborder_acp_rect, Rborder_acp_rect, Bborder_acp_rect) = self.Create_Border_Rect(
            border_acp_surface, self.acp_center_x, self.ans_center_y, self.outline2
        )

        (Lborder_deny_rect, Tborder_deny_rect, Rborder_deny_rect, Bborder_deny_rect) = self.Create_Border_Rect(
            border_deny_surface, self.deny_center_x, self.ans_center_y, self.outline2)

        SCREEN.blit(image, (box_x_position + 250, box_y_position + 150))

        self.Blit_Text_Border(
            text_qs_surface, border_qs_surface, Lborder_qs_rect, Tborder_qs_rect,
            Rborder_qs_rect, Bborder_qs_rect, text_qs_rect
        )

        self.Blit_Text_Border(
            acp_surface, border_acp_surface, Lborder_acp_rect, Tborder_acp_rect,
            Rborder_acp_rect, Bborder_acp_rect, acp_rect
        )

        self.Blit_Text_Border(
            deny_surface, border_deny_surface, Lborder_deny_rect, Tborder_deny_rect,
            Rborder_deny_rect, Bborder_deny_rect, deny_rect
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
    