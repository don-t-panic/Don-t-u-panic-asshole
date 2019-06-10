import pygame
from lib.game.world_objects.world_object import WorldObject

right_sprite = [pygame.image.load('config/assets/main_hero_run_right_0.png'),
                pygame.image.load('config/assets/main_hero_run_right_1.png'),
                pygame.image.load('config/assets/main_hero_run_right_2.png'),
                pygame.image.load('config/assets/main_hero_run_right_3.png'),
                pygame.image.load('config/assets/main_hero_run_right_4.png'),
                pygame.image.load('config/assets/main_hero_run_right_5.png')]

down_sprite = [pygame.image.load('config/assets/main_hero_run_down_0.png'),
               pygame.image.load('config/assets/main_hero_run_down_1.png'),
               pygame.image.load('config/assets/main_hero_run_down_2.png'),
               pygame.image.load('config/assets/main_hero_run_down_3.png')]

left_sprite = [pygame.image.load('config/assets/main_hero_run_left_0.png'),
               pygame.image.load('config/assets/main_hero_run_left_1.png'),
               pygame.image.load('config/assets/main_hero_run_left_2.png'),
               pygame.image.load('config/assets/main_hero_run_left_3.png'),
               pygame.image.load('config/assets/main_hero_run_left_4.png'),
               pygame.image.load('config/assets/main_hero_run_left_5.png')]

up_sprite = [pygame.image.load('config/assets/main_hero_run_up_0.png'),
             pygame.image.load('config/assets/main_hero_run_up_1.png'),
             pygame.image.load('config/assets/main_hero_run_up_2.png'),
             pygame.image.load('config/assets/main_hero_run_up_3.png')]


class Hero(WorldObject):

    def __init__(self, x_coordinate, y_coordinate, hp, nick, items, id, width=40, height=40):
        super().__init__(id, x_coordinate, y_coordinate, width, height)
        self._sprite_path = pygame.image.load('config/assets/main_hero.png')
        self.__hp = 2
        self.__nick = 'elo'
        self.__items = []

