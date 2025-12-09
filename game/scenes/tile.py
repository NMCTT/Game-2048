import pygame

class Tile:
    def __init__(self, value, row, col, x, y, size, font):
        self.value = value
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.size = size
        self.font = font
        
        self.tile_color = (210, 138, 96) 
        self.text_color = (0, 0, 0)
        self.speed = 30
        self.scale = 1
        self.growing_speed = 0.1

    def update_position(self):
        if self.x < self.target_x: self.x = min(self.x + self.speed, self.target_x)
        elif self.x > self.target_x: self.x = max(self.x - self.speed, self.target_x)
        if self.y < self.target_y: self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y: self.y = max(self.y - self.speed, self.target_y)
        if self.scale < 1:
            self.scale += self.growing_speed
            if self.scale > 1: self.scale = 1

    def draw(self, screen):
        current_size = self.size * self.scale
        
        # Tính toán để vẽ TỪ TÂM ra (để khi phóng to nó không bị lệch)
        center_x = self.x + self.size / 2
        center_y = self.y + self.size / 2
        
        rect_x = center_x - current_size / 2
        rect_y = center_y - current_size / 2
        
        rect = pygame.Rect(rect_x, rect_y, current_size, current_size)
        # Tạo khung
        
        # 1. Vẽ ô màu nâu
        pygame.draw.rect(screen, self.tile_color, rect, border_radius=10)
        pygame.draw.rect(screen, (119, 110, 101), rect, width=4, border_radius=10)

        if self.value != 0:
            # Vẽ số
            text_surface = self.font.render(str(self.value), True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.size/2, self.y + self.size/2))
            screen.blit(text_surface, text_rect)