import pygame
from sys import exit
from game.scenes.intro import IntroScene
class App:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption("2048 Game")

        self.clock = pygame.time.Clock()

        self.Intro = IntroScene(self.screen, self.clock) 
        self.current_scence = self.Intro

    def run(self):
        while True:
            next_scene = self.current_scence.run()
            
            if next_scene == "QUIT":
                break
            elif next_scene == "MAIN_GAME":
                break

        pygame.quit()
        exit()


