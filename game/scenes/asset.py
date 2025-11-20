import pygame
from game.settings import SCREEN

screen_width = SCREEN.get_width()
screen_height = SCREEN.get_height()

bg_intro_path = "game/asset/images/intro_background.png"
bg_game_path = "game/asset/images/game_bg.png"
logo_path = "game/asset/images/logo_game.png"
score_path = "game/asset/images/score_layout.png"
exit_path = "game/asset/images/exit_img.png"
back_menu_path = "game/asset/images/back_menu.png"

IMAGE_BACKGROUND = pygame.image.load(bg_intro_path).convert()
IMAGE_GAME_BG = pygame.image.load(bg_game_path).convert()
IMAGE_LOGO = pygame.image.load(logo_path).convert_alpha()
IMAGE_SCORE = pygame.image.load(score_path).convert_alpha()
IMAGE_EXIT_GAME = pygame.image.load(exit_path).convert()
IMAGE_EXIT_BOARD = pygame.image.load(back_menu_path).convert()

IMAGE_SCALED_BACKGROUND = pygame.transform.scale(IMAGE_BACKGROUND, (screen_width, screen_height))
IMAGE_SCALED_GAME_BG = pygame.transform.scale(IMAGE_GAME_BG, (screen_width, screen_height))
IMAGE_SCALED_LOGO = pygame.transform.scale(IMAGE_LOGO, (500, 400))
IMAGE_SCALED_SCORE = pygame.transform.scale(IMAGE_SCORE, (500, 300))
IMAGE_SCALED_EXIT_GAME = pygame.transform.scale(IMAGE_EXIT_GAME, (300, 300))
IMAGE_SCALED_EXIT_BOARD = pygame.transform.scale(IMAGE_EXIT_BOARD, (300, 300))


