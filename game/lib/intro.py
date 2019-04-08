import pygame
from game.lib import gamestates
from game.lib import colors

FONT_STYLE = "Segoe UI"
FONT_SIZE = 0.1


class Intro(object):
    def __init__(self, game):
        self.__game = game
        self.__time_start = pygame.time.get_ticks()
        self.__intro_duration = 6000
        self.__texts = ["Grupa 32", "Presents", "Don\'t u panic a**hole"]
        self.__font = pygame.font.SysFont(FONT_STYLE, int(FONT_SIZE * game.get_screen().get_height()))
        print("Intro initialized")

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game.set_state(gamestates.QUIT)
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__game.set_state(gamestates.LOGIN)
                return
        time_from_start = pygame.time.get_ticks() - self.__time_start
        if time_from_start >= self.__intro_duration:
            self.__game.set_state(gamestates.LOGIN)
            return
        label = self.__font.render(self.__texts[time_from_start // (self.__intro_duration // len(self.__texts))], 1, colors.BLACK)
        label_rect = label.get_rect(center=(self.__game.get_screen().get_width() / 2, self.__game.get_screen().get_height() / 2))
        self.__game.get_screen().blit(label, label_rect)