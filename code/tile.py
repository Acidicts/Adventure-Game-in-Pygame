import pygame 
from settings import *


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		# noinspection PyTypeChecker
		super().__init__(groups)
		self.image = pygame.image.load(BASE_PATH + 'graphics/test/rock.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
