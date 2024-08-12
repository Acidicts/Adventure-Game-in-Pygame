import pygame.sprite

from tile import Tile
from settings import *
from debug import debug
from player import Player


class Level:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.player = None

		self.create_map()

	# noinspection PyTypeChecker
	def create_map(self):
		for row_index, row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
				if col == 'p':
					self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		debug(self.player.direction)


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()

		self.display_Surface = pygame.display.get_surface()

		self.half_width = self.display_Surface.get_width() / 2
		self.half_height = self.display_Surface.get_height() / 2
		self.offset = Vector2(0, 0)

	def custom_draw(self, player):
		self.offset.x = -player.rect.centerx + self.half_width
		self.offset.y = -player.rect.centery + self.half_height

		for sprite in sorted(self.sprites(), key=lambda sprit: sprit.rect.centery):
			offset_pos = sprite.rect.topleft + self.offset
			self.display_Surface.blit(sprite.image, offset_pos)
