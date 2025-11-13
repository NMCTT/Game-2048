import pygame
import os

class IntroScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.menu_items = ["PLAYER MODE", "AI MODE", "EXIT"]
        self.total_menu_items = 3
        self.current_menu_index = 0

        self.dialog_items = ["YES", "NO"]
        self.total_dialog_items = 2
        self.current_dialog_index = 1
        self.dialog_confirm = False

        bg_path = "game/assect/images/intro_background.png"
        exit_path = "game/assect/images/exit_img.png"
        self.bg_image = pygame.image.load(bg_path).convert()
        self.exit_image = pygame.image.load(exit_path).convert()
        screen_width = screen.get_width()  
        screen_height = screen.get_height()
        self.bg_image = pygame.transform.scale(self.bg_image, (screen_width, screen_height))
        self.exit_image = pygame.transform.scale(self.exit_image, (300, 300))


        self.color_normal = (255, 255, 255)
        self.color_choose = (0, 255, 255)
        self.color_border = (0, 0, 0)
        self.color_border_choose = (0, 0, 255)
        self.qs_color = (80, 200, 120)
        self.qs_border = (10, 92, 11)
        self.outline1 = 5
        self.outline2 = 2

        self.defaut_font = pygame.font.Font(pygame.font.get_default_font(), 100)
        self.dialog_font = pygame.font.Font(pygame.font.get_default_font(), 70)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if self.dialog_confirm:
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


                else:
                    if event.type == pygame.KEYDOWN:
                        if (event.key == pygame.K_UP or event.key == pygame.K_w):
                            self.current_menu_index = self.total_menu_items - 1 if (self.current_menu_index == 0) else self.current_menu_index - 1
                        if (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                            self.current_menu_index = 0 if (self.current_menu_index == self.total_menu_items - 1) else self.current_menu_index + 1
                        if (event.key == pygame.K_RETURN):
                            selected_choice = self.menu_items[self.current_menu_index]
                            if (selected_choice == "PLAYER MODE"):
                                return "PLAYER SCENE"
                            if (selected_choice == "AI MODE"):
                                return "AI MODE"
                            if (selected_choice == "EXIT"):
                                self.dialog_confirm = True
                    
            self.screen.blit(self.bg_image, (0,0))

            #Draw Menu Section
            start_x_position = self.screen.get_width() / 2
            start_y_position = (self.screen.get_height() / 2) + 25
            margin_bottom = 50

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
                
            #Draw Dialog When EXIT
            if self.dialog_confirm:
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


            pygame.display.update()
            self.clock.tick(60)
    

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
    