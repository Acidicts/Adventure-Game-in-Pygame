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
		layouts = {
			'boundary': import_csv_layout(BASE_PATH + 'map/map_FloorBlocks.csv'),
		}

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE

						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'grass':
							pass
						if style == 'object':
							pass


		self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()

		self.display_Surface = pygame.display.get_surface()

		self.half_width = self.display_Surface.get_width() / 2
		self.half_height = self.display_Surface.get_height() / 2
		self.offset = Vector2(0, 0)

		self.floor_surf = pygame.image.load(BASE_PATH + 'graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

	def custom_draw(self, player):
		self.offset.x = -player.rect.centerx + self.half_width
		self.offset.y = -player.rect.centery + self.half_height

		self.display_Surface.blit(self.floor_surf, self.offset + self.floor_rect.topleft)

		for sprite in sorted(self.sprites(), key=lambda sprit: sprit.rect.centery):
			offset_pos = sprite.rect.topleft + self.offset
			self.display_Surface.blit(sprite.image, offset_pos)
