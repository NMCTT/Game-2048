import pygame
from sys import exit
from game.scenes.intro import IntroScene
from game.scenes.board import GameScene
class App:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption("2048 Game")

        self.clock = pygame.time.Clock()

        self.Intro = IntroScene(self.screen) 
        self.Board = GameScene(self.screen)
        self.current_scene = self.Intro

        self.dialog_items = ["YES", "NO"]
        self.total_dialog_items = len(self.dialog_items)
        self.current_dialog_index = 1
        self.dialog_confirm = False

        exit_path = "game/asset/images/exit_img.png"
        self.exit_image = pygame.image.load(exit_path).convert()
        screen_width = self.screen.get_width()  
        screen_height = self.screen.get_height()
        self.exit_image = pygame.transform.scale(self.exit_image, (300, 300))

        self.color_normal = (255, 255, 255)
        self.color_choose = (0, 255, 255)
        self.color_border = (0, 0, 0)
        self.color_border_choose = (0, 0, 255)
        self.qs_color = (80, 200, 120)
        self.qs_border = (10, 92, 11)
        self.outline2 = 2

        self.dialog_font = pygame.font.Font(pygame.font.get_default_font(), 70)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.dialog_confirm:
                    signal = self.Handle_Dialog_Event(event) 
                    if signal == "QUIT":
                        running = False
                else:
                    signal = self.current_scene.Handle_Event(event)
                    self.Handle_Signal(signal)
            
            self.current_scene.Draw(self.screen)

            if self.dialog_confirm:
                self.Draw_Exit_Dialog()

            pygame.display.update()
            self.clock.tick(60)

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
                    return "QUIT"
                if (selected_choice == "NO"):
                    self.dialog_confirm = False

    def Handle_Signal(self, signal):
        if signal == "PLAYER MODE":
            self.current_scene = self.Board
        elif signal == "BACK":
            self.current_scene = self.Intro
        elif signal == "AI MODE":
            self.dialog_confirm = False  # FIx khi lam them scene AI mode
        elif signal == "EXIT DIALOG":
            self.dialog_confirm = True
            self.current_dialog_index = 1;

    def Draw_Exit_Dialog(self):
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

        layer_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        layer_surface.fill((0, 0, 0, 150))
        
        self.screen.blit(layer_surface, (0, 0))

        box_width = 800
        box_height = 600
        box_x_position = (self.screen.get_width() - box_width) / 2
        box_y_position = (self.screen.get_height() - box_height) / 2

        dialog_rect = pygame.Rect(box_x_position, box_y_position, box_width, box_height)
        pygame.draw.rect(self.screen, (87,65,48), dialog_rect, 5)
        pygame.draw.rect(self.screen, (193,165,124), dialog_rect, 0, 5)
        
        question = "CONFIRM TO LEAVE??"
        (text_qs_surface, border_qs_surface) = self.Create_Text_Border_Surface(
            self.dialog_font, question, self.qs_color, self.qs_border
        )
        (acp_surface, border_acp_surface) = self.Create_Text_Border_Surface(
            self.dialog_font, self.dialog_items[0], acpColor, acpBorder
        )
        (deny_surface, border_deny_surface) = self.Create_Text_Border_Surface(
            self.dialog_font, self.dialog_items[1], denyColor, denyBorder
        )

        text_center_x = self.screen.get_width() / 2
        text_center_y = (self.screen.get_height() / 2) - 200
        acp_center_x = (self.screen.get_width() / 2) - 150
        deny_center_x = (self.screen.get_width() / 2) + 150
        ans_center_y = (self.screen.get_height() / 2) + 200

        text_qs_rect = text_qs_surface.get_rect(center=(text_center_x, text_center_y))
        acp_rect = acp_surface.get_rect(center=(acp_center_x, ans_center_y))
        deny_rect = deny_surface.get_rect(center=(deny_center_x, ans_center_y))

        (Lborder_qs_rect, Tborder_qs_rect, Rborder_qs_rect, Bborder_qs_rect) = self.Create_Border_Rect(
            border_qs_surface, text_center_x, text_center_y, self.outline2
        )

        (Lborder_acp_rect, Tborder_acp_rect, Rborder_acp_rect, Bborder_acp_rect) = self.Create_Border_Rect(
            border_acp_surface, acp_center_x, ans_center_y, self.outline2
        )

        (Lborder_deny_rect, Tborder_deny_rect, Rborder_deny_rect, Bborder_deny_rect) = self.Create_Border_Rect(
            border_deny_surface, deny_center_x, ans_center_y, self.outline2)

        self.screen.blit(self.exit_image, (box_x_position + 250, box_y_position + 150))

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
        self.screen.blit(border_surface, left)
        self.screen.blit(border_surface, top)
        self.screen.blit(border_surface, right)
        self.screen.blit(border_surface, bottom)
        self.screen.blit(text_surface, rect)
    
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
    